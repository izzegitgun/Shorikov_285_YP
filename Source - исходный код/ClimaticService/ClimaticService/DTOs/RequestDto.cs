using System;

namespace ClimaticService.DTOs
{
    public class CreateRequestDto
    {
        public int TypeId { get; set; }
        public string Model { get; set; } = string.Empty;
        public string ProblemDescription { get; set; } = string.Empty;
        public int ClientId { get; set; }
    }

    public class UpdateRequestDto
    {
        public int? StatusId { get; set; }
        public string? ProblemDescription { get; set; }
        public int? MasterId { get; set; }
        public string? RepairParts { get; set; }
        public DateTime? CompletionDate { get; set; }
    }

    public class AddCommentDto
    {
        public string Message { get; set; } = string.Empty;
        public int MasterId { get; set; }
    }

    public class RequestSearchDto
    {
        public string? SearchTerm { get; set; }
        public int? StatusId { get; set; }
        public int? TypeId { get; set; }
        public DateTime? StartDateFrom { get; set; }
        public DateTime? StartDateTo { get; set; }
    }

    public class LoginDto
    {
        public string Login { get; set; } = string.Empty;
        public string Password { get; set; } = string.Empty;
    }

    public class RegisterDto
    {
        public string Fio { get; set; } = string.Empty;
        public string Phone { get; set; } = string.Empty;
        public string Login { get; set; } = string.Empty;
        public string Password { get; set; } = string.Empty;
        public string Type { get; set; } = "Заказчик";
    }

    /// <summary>Данные для обновления пользователя (редактирование менеджером).</summary>
    public class UpdateUserDto
    {
        public string Fio { get; set; } = string.Empty;
        public string Phone { get; set; } = string.Empty;
        public string Login { get; set; } = string.Empty;
        public string? Password { get; set; }
        public string Type { get; set; } = string.Empty;
    }
}