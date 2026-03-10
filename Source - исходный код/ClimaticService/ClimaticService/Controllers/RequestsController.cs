using ClimaticService.Data;
using ClimaticService.DTOs;
using ClimaticService.Models;
using ClimaticService.Services;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace ClimaticService.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class RequestsController : ControllerBase
    {
        private readonly IRequestService _requestService;
        private readonly ApplicationDbContext _context;
        private readonly ILogger<RequestsController> _logger;
        private readonly FeedbackQrCodeService _feedbackQrCodeService;

        public RequestsController(
            IRequestService requestService,
            ApplicationDbContext context,
            ILogger<RequestsController> logger,
            FeedbackQrCodeService feedbackQrCodeService)
        {
            _requestService = requestService;
            _context = context;
            _logger = logger;
            _feedbackQrCodeService = feedbackQrCodeService;
        }

        // GET: api/requests
        [HttpGet]
        public async Task<IActionResult> GetAllRequests()
        {
            var requests = await _requestService.GetAllRequestsAsync();
            return Ok(requests);
        }

        // GET: api/requests/{id}
        [HttpGet("{id}")]
        public async Task<IActionResult> GetRequestById(int id)
        {
            var request = await _requestService.GetRequestByIdAsync(id);
            if (request == null)
                return NotFound(new { message = $"Заявка с ID {id} не найдена" });

            return Ok(request);
        }

        // POST: api/requests
        [HttpPost]
        public async Task<IActionResult> CreateRequest([FromBody] CreateRequestDto dto)
        {
            try
            {
                var request = await _requestService.CreateRequestAsync(dto);
                return CreatedAtAction(nameof(GetRequestById), new { id = request.RequestId }, request);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Ошибка при создании заявки");
                return BadRequest(new { message = ex.Message });
            }
        }

        // PUT: api/requests/{id}
        [HttpPut("{id}")]
        public async Task<IActionResult> UpdateRequest(int id, [FromBody] UpdateRequestDto dto)
        {
            var request = await _requestService.UpdateRequestAsync(id, dto);
            if (request == null)
                return NotFound(new { message = $"Заявка с ID {id} не найдена" });

            return Ok(request);
        }

        // DELETE: api/requests/{id}
        [HttpDelete("{id}")]
        public async Task<IActionResult> DeleteRequest(int id)
        {
            var deleted = await _requestService.DeleteRequestAsync(id);
            if (!deleted)
                return NotFound(new { message = $"Заявка с ID {id} не найдена" });
            return Ok(new { message = "Заявка удалена" });
        }

        // POST: api/requests/{id}/assign-master/{masterId}
        [HttpPost("{id}/assign-master/{masterId}")]
        public async Task<IActionResult> AssignMaster(int id, int masterId)
        {
            var request = await _requestService.AssignMasterAsync(id, masterId);
            if (request == null)
                return NotFound(new { message = $"Заявка с ID {id} не найдена" });

            return Ok(new { message = "Мастер назначен", request });
        }

        // POST: api/requests/{id}/status/{statusId}
        [HttpPost("{id}/status/{statusId}")]
        public async Task<IActionResult> UpdateStatus(int id, int statusId)
        {
            var request = await _requestService.UpdateStatusAsync(id, statusId);
            if (request == null)
                return NotFound(new { message = $"Заявка с ID {id} не найдена" });

            return Ok(new { message = "Статус обновлен", request });
        }

        // POST: api/requests/search
        [HttpPost("search")]
        public async Task<IActionResult> SearchRequests([FromBody] RequestSearchDto searchDto)
        {
            var requests = await _requestService.SearchRequestsAsync(searchDto);
            return Ok(requests);
        }

        // GET: api/requests/client/{clientId}
        [HttpGet("client/{clientId}")]
        public async Task<IActionResult> GetClientRequests(int clientId)
        {
            var requests = await _context.Requests
                .Include(r => r.Status)
                .Include(r => r.EquipmentType)
                .Include(r => r.Master)
                .Where(r => r.ClientId == clientId)
                .OrderByDescending(r => r.StartDate)
                .ToListAsync();

            return Ok(requests);
        }

        // GET: api/requests/master/{masterId}
        [HttpGet("master/{masterId}")]
        public async Task<IActionResult> GetMasterRequests(int masterId)
        {
            var requests = await _context.Requests
                .Include(r => r.Client)
                .Include(r => r.Status)
                .Include(r => r.EquipmentType)
                .Where(r => r.MasterId == masterId)
                .OrderByDescending(r => r.StartDate)
                .ToListAsync();

            return Ok(requests);
        }

        // GET: api/requests/types
        [HttpGet("types")]
        public async Task<IActionResult> GetEquipmentTypes()
        {
            var types = await _context.ClimateTechTypes.ToListAsync();
            return Ok(types);
        }

        // GET: api/requests/statuses
        [HttpGet("statuses")]
        public async Task<IActionResult> GetStatuses()
        {
            var statuses = await _context.RequestStatuses.ToListAsync();
            return Ok(statuses);
        }

        // POST: api/requests/{id}/comments
        [HttpPost("{id}/comments")]
        public async Task<IActionResult> AddComment(int id, [FromBody] AddCommentDto dto)
        {
            var comment = await _requestService.AddCommentAsync(id, dto);
            return Ok(comment);
        }

        // GET: api/requests/{id}/comments
        [HttpGet("{id}/comments")]
        public async Task<IActionResult> GetComments(int id)
        {
            var comments = await _requestService.GetCommentsAsync(id);
            return Ok(comments);
        }

        // GET: api/requests/statistics
        [HttpGet("statistics")]
        public async Task<IActionResult> GetStatistics()
        {
            var statistics = await _requestService.GetStatisticsAsync();
            return Ok(statistics);
        }

        // POST: api/requests/{id}/extend-deadline
        [HttpPost("{id}/extend-deadline")]
        public async Task<IActionResult> ExtendDeadline(int id, [FromBody] ExtendDeadlineDto dto)
        {
            try
            {
                var request = await _requestService.ExtendDeadlineAsync(id, dto);
                if (request == null)
                    return NotFound(new { message = $"Заявка с ID {id} не найдена" });

                return Ok(new { message = "Срок выполнения заявки продлён", request });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Ошибка при продлении срока выполнения заявки");
                return BadRequest(new { message = ex.Message });
            }
        }

        // POST: api/requests/{id}/quality-help
        [HttpPost("{id}/quality-help")]
        public async Task<IActionResult> RequestQualityHelp(int id, [FromBody] RequestQualityHelpDto dto)
        {
            try
            {
                var request = await _requestService.RequestQualityHelpAsync(id, dto);
                if (request == null)
                    return NotFound(new { message = $"Заявка с ID {id} не найдена" });

                return Ok(new { message = "Запрос на помощь менеджера по качеству отправлен", request });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Ошибка при запросе помощи менеджера по качеству");
                return BadRequest(new { message = ex.Message });
            }
        }

        // GET: api/requests/{id}/feedback-qr
        [HttpGet("{id}/feedback-qr")]
        public IActionResult GetFeedbackQr(int id)
        {
            var bytes = _feedbackQrCodeService.GenerateFeedbackQrCode(id);
            return File(bytes, "image/png");
        }
    }
}