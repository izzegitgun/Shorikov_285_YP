using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace ClimaticService.Models
{
    [Table("request_statuses")]
    public class RequestStatus
    {
        [Key]
        [Column("status_id")]
        public int StatusId { get; set; }

        [Column("status_name")]
        [Required]
        [MaxLength(50)]
        public string StatusName { get; set; } = string.Empty;

        [Column("status_description")]
        public string? StatusDescription { get; set; }
    }
}