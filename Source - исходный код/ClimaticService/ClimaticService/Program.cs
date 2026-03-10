using ClimaticService.Data;
using ClimaticService.Services;
using Microsoft.EntityFrameworkCore;
using Microsoft.AspNetCore.Builder;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using System.Diagnostics;
using System.Runtime.InteropServices;
using Npgsql;

var builder = WebApplication.CreateBuilder(args);

// Включаем поддержку локальных временных меток для Npgsql
AppContext.SetSwitch("Npgsql.EnableLegacyTimestampBehavior", true);

builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

// Регистрируем сервисы
builder.Services.AddScoped<IRequestService, RequestService>();
builder.Services.AddScoped<FeedbackQrCodeService>();

// Подключение к БД
builder.Services.AddDbContext<ApplicationDbContext>(options =>
    options.UseNpgsql(builder.Configuration.GetConnectionString("DefaultConnection")));

// CORS
builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowAll", policy =>
    {
        policy.AllowAnyOrigin()
              .AllowAnyMethod()
              .AllowAnyHeader();
    });
});

var app = builder.Build();

if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();

// Добавляем поддержку статических файлов
app.UseDefaultFiles(new DefaultFilesOptions
{
    DefaultFileNames = new List<string> { "login.html" }
});
app.UseStaticFiles();

app.UseCors("AllowAll");
app.UseAuthorization();
app.MapControllers();

// Инициализация БД
using (var scope = app.Services.CreateScope())
{
    var dbContext = scope.ServiceProvider.GetRequiredService<ApplicationDbContext>();

    try
    {
        if (dbContext.Database.CanConnect())
        {
            Console.WriteLine("✓ Подключение к базе данных успешно установлено");

            var userCount = await dbContext.Users.CountAsync();
            Console.WriteLine($"✓ В базе данных найдено {userCount} пользователей");
        }
        else
        {
            Console.WriteLine("✗ Ошибка подключения к базе данных");
        }
    }
    catch (Exception ex)
    {
        Console.WriteLine($"✗ Ошибка при проверке базы данных: {ex.Message}");
    }
}

var url = "https://localhost:7233/login.html";

Console.WriteLine("🚀 Запуск ClimaticService...");
Console.WriteLine($"📱 Открытие страницы входа: {url}");

try
{
    if (RuntimeInformation.IsOSPlatform(OSPlatform.Windows))
    {
        Process.Start(new ProcessStartInfo(url) { UseShellExecute = true });
    }
    else if (RuntimeInformation.IsOSPlatform(OSPlatform.Linux))
    {
        Process.Start("xdg-open", url);
    }
    else if (RuntimeInformation.IsOSPlatform(OSPlatform.OSX))
    {
        Process.Start("open", url);
    }
}
catch (Exception ex)
{
    Console.WriteLine($"Не удалось автоматически открыть браузер: {ex.Message}");
    Console.WriteLine($"Пожалуйста, откройте вручную: {url}");
}

app.Run();