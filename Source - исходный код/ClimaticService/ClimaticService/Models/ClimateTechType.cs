using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace ClimaticService.Models
{
    [Table("climate_tech_types")]
    public class ClimateTechType
    {
        [Key]
        [Column("type_id")]
        public int TypeId { get; set; }

        [Column("type_name")]
        [Required]
        [MaxLength(50)]
        public string TypeName { get; set; } = string.Empty;

        [Column("type_description")]
        public string? TypeDescription { get; set; }
    }
}