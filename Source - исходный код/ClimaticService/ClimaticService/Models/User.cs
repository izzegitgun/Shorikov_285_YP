using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace ClimaticService.Models
{
    [Table("users")]
    public class User
    {
        [Key]
        [Column("user_id")]
        public int UserId { get; set; }

        [Column("fio")]
        [Required]
        [MaxLength(100)]
        public string Fio { get; set; } = string.Empty;

        [Column("phone")]
        [Required]
        [MaxLength(20)]
        public string Phone { get; set; } = string.Empty;

        [Column("login")]
        [Required]
        [MaxLength(50)]
        public string Login { get; set; } = string.Empty;

        [Column("password")]
        [Required]
        [MaxLength(255)]
        public string Password { get; set; } = string.Empty;

        [Column("type")]
        [Required]
        [MaxLength(20)]
        public string Type { get; set; } = string.Empty;

        [Column("is_deleted")]
        public bool IsDeleted { get; set; }
    }
}