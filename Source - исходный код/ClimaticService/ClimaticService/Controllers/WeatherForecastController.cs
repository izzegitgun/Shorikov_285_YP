using Microsoft.AspNetCore.Mvc;
using ClimaticService.Data;
using Microsoft.EntityFrameworkCore;

namespace ClimaticService.Controllers;

[ApiController]
[Route("api/[controller]")]
public class TestController : ControllerBase
{
    private readonly ApplicationDbContext _context;

    public TestController(ApplicationDbContext context)
    {
        _context = context;
    }

    [HttpGet("users")]
    public async Task<IActionResult> GetUsers()
    {
        var users = await _context.Users.ToListAsync();
        return Ok(users);
    }

    [HttpGet("requests")]
    public async Task<IActionResult> GetRequests()
    {
        var requests = await _context.Requests
            .Include(r => r.Client)
            .Include(r => r.Master)
            .Include(r => r.EquipmentType)
            .Include(r => r.Status)
            .ToListAsync();
        return Ok(requests);
    }

    [HttpGet("check")]
    public IActionResult CheckConnection()
    {
        try
        {
            var canConnect = _context.Database.CanConnect();
            return Ok(new { connected = canConnect, message = "Подключение к БД успешно!" });
        }
        catch (Exception ex)
        {
            return BadRequest(new { connected = false, error = ex.Message });
        }
    }
}