using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Storage.ValueConversion;
using ClimaticService.Models;

namespace ClimaticService.Data
{
    public class ApplicationDbContext : DbContext
    {
        public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options)
            : base(options)
        {
        }

        public DbSet<User> Users { get; set; }
        public DbSet<ClimateTechType> ClimateTechTypes { get; set; }
        public DbSet<RequestStatus> RequestStatuses { get; set; }
        public DbSet<Request> Requests { get; set; }
        public DbSet<Comment> Comments { get; set; }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            base.OnModelCreating(modelBuilder);

            var dateTimeConverter = new ValueConverter<DateTime, DateTime>(
                v => v.ToUniversalTime(),
                v => DateTime.SpecifyKind(v, DateTimeKind.Utc));

            var nullableDateTimeConverter = new ValueConverter<DateTime?, DateTime?>(
                v => v.HasValue ? v.Value.ToUniversalTime() : v,
                v => v.HasValue ? DateTime.SpecifyKind(v.Value, DateTimeKind.Utc) : v);

            foreach (var entityType in modelBuilder.Model.GetEntityTypes())
            {
                foreach (var property in entityType.GetProperties())
                {
                    if (property.ClrType == typeof(DateTime))
                    {
                        property.SetValueConverter(dateTimeConverter);
                    }
                    else if (property.ClrType == typeof(DateTime?))
                    {
                        property.SetValueConverter(nullableDateTimeConverter);
                    }
                }
            }

            modelBuilder.Entity<User>(entity =>
            {
                entity.ToTable("users");
                entity.HasKey(e => e.UserId);
                entity.HasIndex(e => e.Login).IsUnique();
            });

            modelBuilder.Entity<ClimateTechType>(entity =>
            {
                entity.ToTable("climate_tech_types");
                entity.HasKey(e => e.TypeId);
                entity.HasIndex(e => e.TypeName).IsUnique();
            });

            modelBuilder.Entity<RequestStatus>(entity =>
            {
                entity.ToTable("request_statuses");
                entity.HasKey(e => e.StatusId);
                entity.HasIndex(e => e.StatusName).IsUnique();
            });

            modelBuilder.Entity<Request>(entity =>
            {
                entity.ToTable("requests");
                entity.HasKey(e => e.RequestId);

                // Указываем тип колонок для дат
                entity.Property(e => e.StartDate)
                    .HasColumnType("timestamp with time zone");

                entity.Property(e => e.CompletionDate)
                    .HasColumnType("timestamp with time zone");

                entity.HasOne(e => e.EquipmentType)
                    .WithMany()
                    .HasForeignKey(e => e.TypeId)
                    .OnDelete(DeleteBehavior.Restrict);

                entity.HasOne(e => e.Status)
                    .WithMany()
                    .HasForeignKey(e => e.StatusId)
                    .OnDelete(DeleteBehavior.Restrict);

                entity.HasOne(e => e.Master)
                    .WithMany()
                    .HasForeignKey(e => e.MasterId)
                    .OnDelete(DeleteBehavior.SetNull);

                entity.HasOne(e => e.Client)
                    .WithMany()
                    .HasForeignKey(e => e.ClientId)
                    .OnDelete(DeleteBehavior.Restrict);
            });

            modelBuilder.Entity<Comment>(entity =>
            {
                entity.ToTable("comments");
                entity.HasKey(e => e.CommentId);

                entity.HasOne(e => e.Author)
                    .WithMany()
                    .HasForeignKey(e => e.MasterId)
                    .OnDelete(DeleteBehavior.Cascade);

                entity.HasOne(e => e.Request)
                    .WithMany()
                    .HasForeignKey(e => e.RequestId)
                    .OnDelete(DeleteBehavior.Cascade);
            });
        }
    }
}