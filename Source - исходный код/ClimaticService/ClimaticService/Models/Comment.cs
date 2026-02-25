using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace ClimaticService.Models
{
    [Table("comments")]
    public class Comment
    {
        [Key]
        [Column("comment_id")]
        public int CommentId { get; set; }

        [Column("message")]
        [Required]
        public string Message { get; set; } = string.Empty;

        [Column("master_id")]
        [Required]
        public int MasterId { get; set; }

        [Column("request_id")]
        [Required]
        public int RequestId { get; set; }

        [ForeignKey("MasterId")]
        public User? Author { get; set; }

        [ForeignKey("RequestId")]
        public Request? Request { get; set; }
    }
}