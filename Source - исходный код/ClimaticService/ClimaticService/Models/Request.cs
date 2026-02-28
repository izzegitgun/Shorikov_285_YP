using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace ClimaticService.Models
{
    [Table("requests")]
    public class Request
    {
        [Key]
        [Column("request_id")]
        public int RequestId { get; set; }

        [Column("start_date")]
        [Required]
        public DateTime StartDate { get; set; }

        [Column("type_id")]
        [Required]
        public int TypeId { get; set; }

        [Column("model")]
        [Required]
        [MaxLength(100)]
        public string Model { get; set; } = string.Empty;

        [Column("problem_description")]
        [Required]
        public string ProblemDescription { get; set; } = string.Empty;

        [Column("status_id")]
        [Required]
        public int StatusId { get; set; }

        [Column("completion_date")]
        public DateTime? CompletionDate { get; set; }

        [Column("repair_parts")]
        public string? RepairParts { get; set; }

        [Column("master_id")]
        public int? MasterId { get; set; }

        [Column("client_id")]
        [Required]
        public int ClientId { get; set; }

        [Column("quality_manager_id")]
        public int? QualityManagerId { get; set; }

        [Column("deadline_extended")]
        public bool DeadlineExtended { get; set; }

        [ForeignKey("TypeId")]
        public ClimateTechType? EquipmentType { get; set; }

        [ForeignKey("StatusId")]
        public RequestStatus? Status { get; set; }

        [ForeignKey("MasterId")]
        public User? Master { get; set; }

        [ForeignKey("ClientId")]
        public User? Client { get; set; }
    }
}