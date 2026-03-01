using ClimaticService.Data;
using ClimaticService.DTOs;
using ClimaticService.Models;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using System.Text.Json;

namespace ClimaticService.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class AuthController : ControllerBase
    {
        private readonly ApplicationDbContext _context;
        private readonly ILogger<AuthController> _logger;

        public AuthController(ApplicationDbContext context, ILogger<AuthController> logger)
        {
            _context = context;
            _logger = logger;
        }

        [HttpPost("login")]
        public async Task<IActionResult> Login([FromBody] LoginDto loginDto)
        {
            try
            {
                // Ищем пользователя по логину
                var user = await _context.Users
                    .FirstOrDefaultAsync(u => u.Login == loginDto.Login && !u.IsDeleted);

                if (user == null)
                {
                    return Unauthorized(new { message = "Неверный логин или пароль" });
                }

                // Проверяем пароль (в вашей БД пароли хранятся в открытом виде)
                // В реальном проекте нужно использовать хеширование!
                if (user.Password != loginDto.Password)
                {
                    return Unauthorized(new { message = "Неверный логин или пароль" });
                }

                // Не возвращаем пароль в ответе
                var userResponse = new
                {
                    user.UserId,
                    user.Fio,
                    user.Phone,
                    user.Login,
                    user.Type,
                    user.IsDeleted
                };

                return Ok(new
                {
                    user = userResponse,
                    message = "Вход выполнен успешно",
                    token = Guid.NewGuid().ToString() // Для простоты используем GUID, в реальном проекте - JWT
                });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Ошибка при входе");
                return StatusCode(500, new { message = "Внутренняя ошибка сервера" });
            }
        }

        [HttpPost("register")]
        public async Task<IActionResult> Register([FromBody] RegisterDto registerDto)
        {
            try
            {
                // Проверяем, существует ли пользователь с таким логином
                var existingUser = await _context.Users
                    .FirstOrDefaultAsync(u => u.Login == registerDto.Login);

                if (existingUser != null)
                {
                    return BadRequest(new { message = "Пользователь с таким логином уже существует" });
                }

                var user = new User
                {
                    Fio = registerDto.Fio,
                    Phone = registerDto.Phone,
                    Login = registerDto.Login,
                    Password = registerDto.Password, // В реальном проекте нужно хешировать!
                    Type = registerDto.Type,
                    IsDeleted = false
                };

                _context.Users.Add(user);
                await _context.SaveChangesAsync();

                var userResponse = new
                {
                    user.UserId,
                    user.Fio,
                    user.Phone,
                    user.Login,
                    user.Type
                };

                return Ok(new
                {
                    user = userResponse,
                    message = "Регистрация успешна"
                });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Ошибка при регистрации");
                return StatusCode(500, new { message = "Внутренняя ошибка сервера" });
            }
        }

        // ========== Пользователи (страница «Пользователи», ролевая модель) ==========

        /// <summary>Список пользователей (для страницы «Пользователи»). Логин возвращаем для отображения.</summary>
        [HttpGet("users")]
        public async Task<IActionResult> GetUsers()
        {
            var users = await _context.Users
                .Where(u => !u.IsDeleted)
                .Select(u => new { u.UserId, u.Fio, u.Phone, u.Login, u.Type })
                .ToListAsync();
            return Ok(users);
        }

        /// <summary>Обновление пользователя. Только менеджер (проверка по заголовку X-Current-User-Id).</summary>
        [HttpPut("users/{id}")]
        public async Task<IActionResult> UpdateUser(int id, [FromBody] UpdateUserDto dto)
        {
            if (!Request.Headers.TryGetValue("X-Current-User-Id", out var currentUserIdHeader) ||
                !int.TryParse(currentUserIdHeader, out var currentUserId))
            {
                return Forbid();
            }

            var currentUser = await _context.Users.FindAsync(currentUserId);
            if (currentUser == null || (currentUser.Type != "Менеджер" && currentUser.Type != "Менеджер по качеству"))
            {
                return Forbid();
            }

            var user = await _context.Users.FindAsync(id);
            if (user == null || user.IsDeleted)
            {
                return NotFound(new { message = "Пользователь не найден" });
            }

            user.Fio = dto.Fio;
            user.Phone = dto.Phone;
            user.Login = dto.Login;
            if (!string.IsNullOrWhiteSpace(dto.Password))
            {
                user.Password = dto.Password;
            }
            user.Type = dto.Type;
            await _context.SaveChangesAsync();

            return Ok(new { user.UserId, user.Fio, user.Phone, user.Login, user.Type });
        }

        /// <summary>Мягкое удаление пользователя. Только менеджер.</summary>
        [HttpDelete("users/{id}")]
        public async Task<IActionResult> DeleteUser(int id)
        {
            if (!Request.Headers.TryGetValue("X-Current-User-Id", out var currentUserIdHeader) ||
                !int.TryParse(currentUserIdHeader, out var currentUserId))
            {
                return Forbid();
            }

            var currentUser = await _context.Users.FindAsync(currentUserId);
            if (currentUser == null || (currentUser.Type != "Менеджер" && currentUser.Type != "Менеджер по качеству"))
            {
                return Forbid();
            }

            var user = await _context.Users.FindAsync(id);
            if (user == null || user.IsDeleted)
            {
                return NotFound(new { message = "Пользователь не найден" });
            }

            user.IsDeleted = true;
            await _context.SaveChangesAsync();
            return Ok(new { message = "Пользователь удалён" });
        }

        [HttpGet("masters")]
        public async Task<IActionResult> GetMasters()
        {
            var masters = await _context.Users
                .Where(u => u.Type == "Специалист" && !u.IsDeleted)
                .Select(u => new { u.UserId, u.Fio, u.Phone })
                .ToListAsync();
            return Ok(masters);
        }

        [HttpGet("check/{login}")]
        public async Task<IActionResult> CheckLoginExists(string login)
        {
            var exists = await _context.Users
                .AnyAsync(u => u.Login == login);
            return Ok(new { exists });
        }
    }
}