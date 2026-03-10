using ClimaticService.DTOs;
using ClimaticService.Models;

namespace ClimaticService.Services
{
    public interface IRequestService
    {
        Task<IEnumerable<Request>> GetAllRequestsAsync();
        Task<Request?> GetRequestByIdAsync(int id);
        Task<Request> CreateRequestAsync(CreateRequestDto dto);
        Task<Request?> UpdateRequestAsync(int id, UpdateRequestDto dto);
        Task<bool> DeleteRequestAsync(int id);
        Task<Request?> AssignMasterAsync(int requestId, int masterId);
        Task<Request?> UpdateStatusAsync(int requestId, int statusId);
        Task<IEnumerable<Request>> SearchRequestsAsync(RequestSearchDto searchDto);
        Task<Comment> AddCommentAsync(int requestId, AddCommentDto dto);
        Task<IEnumerable<Comment>> GetCommentsAsync(int requestId);
        Task<object> GetStatisticsAsync();
        Task<bool> NotifyClientAsync(int requestId, string message);
        Task<Request?> ExtendDeadlineAsync(int requestId, ExtendDeadlineDto dto);
        Task<Request?> RequestQualityHelpAsync(int requestId, RequestQualityHelpDto dto);
    }
}