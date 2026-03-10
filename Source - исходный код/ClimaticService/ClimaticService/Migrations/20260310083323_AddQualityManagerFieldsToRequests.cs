using System;
using Microsoft.EntityFrameworkCore.Migrations;
using Npgsql.EntityFrameworkCore.PostgreSQL.Metadata;

#nullable disable

namespace ClimaticService.Migrations
{
    /// <inheritdoc />
    public partial class AddQualityManagerFieldsToRequests : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            // База уже содержит таблицы; добавляем только новые поля к существующей таблице requests
            migrationBuilder.AddColumn<DateTime>(
                name: "planned_completion_date",
                table: "requests",
                type: "timestamp without time zone",
                nullable: true);

            migrationBuilder.AddColumn<string>(
                name: "technician_problem_description",
                table: "requests",
                type: "text",
                nullable: true);

            migrationBuilder.AddColumn<string>(
                name: "quality_manager_comment",
                table: "requests",
                type: "text",
                nullable: true);

            migrationBuilder.AddColumn<string>(
                name: "customer_approval_note",
                table: "requests",
                type: "text",
                nullable: true);
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropColumn(
                name: "planned_completion_date",
                table: "requests");

            migrationBuilder.DropColumn(
                name: "technician_problem_description",
                table: "requests");

            migrationBuilder.DropColumn(
                name: "quality_manager_comment",
                table: "requests");

            migrationBuilder.DropColumn(
                name: "customer_approval_note",
                table: "requests");
        }
    }
}
