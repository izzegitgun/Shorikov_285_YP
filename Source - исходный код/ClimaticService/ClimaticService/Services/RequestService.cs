using ClimaticService.Data;
using ClimaticService.DTOs;
using ClimaticService.Models;
using Microsoft.EntityFrameworkCore;

namespace ClimaticService.Services
{
    public class RequestService : IRequestService
    {
        private readonly ApplicationDbContext _context;
        private readonly ILogger<RequestService> _logger;

        public RequestService(ApplicationDbContext context, ILogger<RequestService> logger)
        {
            _context = context;
            _logger = logger;
        }

        public async Task<IEnumerable<Request>> GetAllRequestsAsync()
        {
            return await _context.Requests
                .Include(r => r.Client)
                .Include(r => r.Master)
                .Include(r => r.EquipmentType)
                .Include(r => r.Status)
                .OrderByDescending(r => r.StartDate)
                .ToListAsync();
        }

        public async Task<Request?> GetRequestByIdAsync(int id)
        {
            return await _context.Requests
                .Include(r => r.Client)
                .Include(r => r.Master)
                .Include(r => r.EquipmentType)
                .Include(r => r.Status)
                .FirstOrDefaultAsync(r => r.RequestId == id);
        }

        public async Task<Request> CreateRequestAsync(CreateRequestDto dto)
        {
            var request = new Request
            {
                // Используем UtcNow вместо Now
                StartDate = DateTime.UtcNow,
                TypeId = dto.TypeId,
                Model = dto.Model,
                ProblemDescription = dto.ProblemDescription,
                StatusId = 1, // "Новая заявка"
                ClientId = dto.ClientId,
                DeadlineExtended = false
            };

            _context.Requests.Add(request);
            await _context.SaveChangesAsync();

            // Уведомляем менеджеров о новой заявке
            await NotifyManagersAsync($"Поступила новая заявка #{request.RequestId}");

            return request;
        }

        public async Task<Request?> UpdateRequestAsync(int id, UpdateRequestDto dto)
        {
            var request = await _context.Requests.FindAsync(id);
            if (request == null) return null;

            var oldStatusId = request.StatusId;

            if (dto.StatusId != null)
                request.StatusId = dto.StatusId.Value;

            if (!string.IsNullOrEmpty(dto.ProblemDescription))
                request.ProblemDescription = dto.ProblemDescription;

            if (dto.MasterId != null)
                request.MasterId = dto.MasterId.Value;

            if (!string.IsNullOrEmpty(dto.RepairParts))
                request.RepairParts = dto.RepairParts;

            if (dto.CompletionDate != null)
                // Конвертируем в UTC если это локальное время
                request.CompletionDate = dto.CompletionDate.Value.Kind == DateTimeKind.Local
                    ? dto.CompletionDate.Value.ToUniversalTime()
                    : dto.CompletionDate.Value;

            await _context.SaveChangesAsync();

            if (oldStatusId != request.StatusId && request.ClientId > 0)
            {
                var status = await _context.RequestStatuses.FindAsync(request.StatusId);
                await NotifyClientAsync(request.RequestId,
                    $"Статус вашей заявки #{request.RequestId} изменен на '{status?.StatusName}'");
            }

            return request;
        }

        public async Task<bool> DeleteRequestAsync(int id)
        {
            var request = await _context.Requests.FindAsync(id);
            if (request == null) return false;
            _context.Requests.Remove(request);
            await _context.SaveChangesAsync();
            return true;
        }

        public async Task<Request?> AssignMasterAsync(int requestId, int masterId)
        {
            var request = await _context.Requests.FindAsync(requestId);
            if (request == null) return null;

            request.MasterId = masterId;
            if (request.StatusId == 1) 
            {
                request.StatusId = 2;
            }

            await _context.SaveChangesAsync();

            var master = await _context.Users.FindAsync(masterId);
            await NotifyMasterAsync(masterId,
                $"Вам назначена заявка #{request.RequestId}");

            return request;
        }

        public async Task<Request?> UpdateStatusAsync(int requestId, int statusId)
        {
            var request = await _context.Requests.FindAsync(requestId);
            if (request == null) return null;

            var oldStatusId = request.StatusId;
            request.StatusId = statusId;

            if (statusId == 3) // Если статус "Завершена"
            {
                // Используем UtcNow
                request.CompletionDate = DateTime.UtcNow;
            }

            await _context.SaveChangesAsync();

            var status = await _context.RequestStatuses.FindAsync(statusId);
            await NotifyClientAsync(requestId,
                $"Статус вашей заявки #{requestId} изменен на '{status?.StatusName}'");

            return request;
        }

        public async Task<IEnumerable<Request>> SearchRequestsAsync(RequestSearchDto searchDto)
        {
            var query = _context.Requests
                .Include(r => r.Client)
                .Include(r => r.Master)
                .Include(r => r.EquipmentType)
                .Include(r => r.Status)
                .AsQueryable();

            if (!string.IsNullOrEmpty(searchDto.SearchTerm))
            {
                var searchTerm = searchDto.SearchTerm.ToLower();
                query = query.Where(r =>
                    r.RequestId.ToString().Contains(searchTerm) ||
                    (r.Client != null && r.Client.Fio.ToLower().Contains(searchTerm)) ||
                    r.Model.ToLower().Contains(searchTerm) ||
                    r.ProblemDescription.ToLower().Contains(searchTerm));
            }

            if (searchDto.StatusId != null)
                query = query.Where(r => r.StatusId == searchDto.StatusId.Value);

            if (searchDto.TypeId != null)
                query = query.Where(r => r.TypeId == searchDto.TypeId.Value);

            if (searchDto.StartDateFrom != null)
                // Конвертируем в UTC для поиска
                query = query.Where(r => r.StartDate >= searchDto.StartDateFrom.Value.ToUniversalTime());

            if (searchDto.StartDateTo != null)
                query = query.Where(r => r.StartDate <= searchDto.StartDateTo.Value.ToUniversalTime());

            return await query.OrderByDescending(r => r.StartDate).ToListAsync();
        }

        public async Task<Comment> AddCommentAsync(int requestId, AddCommentDto dto)
        {
            var comment = new Comment
            {
                Message = dto.Message,
                MasterId = dto.MasterId,
                RequestId = requestId
            };

            _context.Comments.Add(comment);
            await _context.SaveChangesAsync();

            return comment;
        }

        public async Task<IEnumerable<Comment>> GetCommentsAsync(int requestId)
        {
            return await _context.Comments
                .Include(c => c.Author)
                .Where(c => c.RequestId == requestId)
                .OrderByDescending(c => c.CommentId)
                .ToListAsync();
        }

        public async Task<object> GetStatisticsAsync()
        {
            var requests = await _context.Requests.ToListAsync();
            var completedRequests = requests.Where(r => r.CompletionDate.HasValue).ToList();

            // Среднее время выполнения (в днях)
            double avgTime = 0;
            if (completedRequests.Any())
            {
                avgTime = completedRequests
                    .Select(r => (r.CompletionDate!.Value - r.StartDate).TotalDays)
                    .Average();
            }

            // Статистика по типам неисправностей
            var faultTypes = await _context.Requests
                .GroupBy(r => r.TypeId)
                .Select(g => new {
                    TypeId = g.Key,
                    Count = g.Count(),
                    TypeName = _context.ClimateTechTypes
                        .Where(t => t.TypeId == g.Key)
                        .Select(t => t.TypeName)
                        .FirstOrDefault() ?? "Неизвестно"
                })
                .OrderByDescending(x => x.Count)
                .ToListAsync();

            // Статистика по статусам
            var statusStats = await _context.Requests
                .GroupBy(r => r.StatusId)
                .Select(g => new {
                    StatusId = g.Key,
                    Count = g.Count(),
                    StatusName = _context.RequestStatuses
                        .Where(s => s.StatusId == g.Key)
                        .Select(s => s.StatusName)
                        .FirstOrDefault() ?? "Неизвестно"
                })
                .ToListAsync();

            return new
            {
                TotalRequests = requests.Count,
                CompletedRequests = completedRequests.Count,
                InProgressRequests = requests.Count(r => r.StatusId == 2),
                NewRequests = requests.Count(r => r.StatusId == 1),
                AverageCompletionTimeDays = Math.Round(avgTime, 1),
                FaultTypeStatistics = faultTypes,
                StatusStatistics = statusStats
            };
        }

        public async Task<bool> NotifyClientAsync(int requestId, string message)
        {
            try
            {
                var request = await _context.Requests
                    .Include(r => r.Client)
                    .FirstOrDefaultAsync(r => r.RequestId == requestId);

                if (request?.Client == null) return false;

                _logger.LogInformation($"Уведомление для клиента {request.Client.Fio}: {message}");


                return true;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Ошибка при отправке уведомления клиенту");
                return false;
            }
        }

        private async Task NotifyManagersAsync(string message)
        {
            var managers = await _context.Users
                .Where(u => u.Type == "Менеджер по качеству" && !u.IsDeleted)
                .ToListAsync();

            foreach (var manager in managers)
            {
                _logger.LogInformation($"Уведомление для менеджера {manager.Fio}: {message}");
            }
        }

        private async Task NotifyMasterAsync(int masterId, string message)
        {
            var master = await _context.Users.FindAsync(masterId);
            if (master != null)
            {
                _logger.LogInformation($"Уведомление для мастера {master.Fio}: {message}");
            }
        }
    }
}