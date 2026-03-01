using ClimaticService.Models;
using Microsoft.EntityFrameworkCore;

namespace ClimaticService.Data
{
    public static class SeedData
    {
        public static async Task Initialize(ApplicationDbContext context)
        {
            // Добавляем статусы заявок
            if (!await context.RequestStatuses.AnyAsync())
            {
                var statuses = new[]
                {
                    new RequestStatus { StatusName = "Новая заявка", StatusDescription = "Только что создана" },
                    new RequestStatus { StatusName = "В процессе ремонта", StatusDescription = "Принята в работу" },
                    new RequestStatus { StatusName = "Ожидание комплектующих", StatusDescription = "Ожидание запчастей" },
                    new RequestStatus { StatusName = "Завершена", StatusDescription = "Работа выполнена" },
                    new RequestStatus { StatusName = "Отменена", StatusDescription = "Заявка отменена" }
                };
                await context.RequestStatuses.AddRangeAsync(statuses);
                await context.SaveChangesAsync();
            }

            // Добавляем типы оборудования
            if (!await context.ClimateTechTypes.AnyAsync())
            {
                var types = new[]
                {
                    new ClimateTechType { TypeName = "Кондиционер", TypeDescription = "Сплит-системы, мульти-сплит системы" },
                    new ClimateTechType { TypeName = "Вентиляция", TypeDescription = "Приточные и вытяжные установки" },
                    new ClimateTechType { TypeName = "Обогреватель", TypeDescription = "Масляные, инфракрасные, конвекторы" },
                    new ClimateTechType { TypeName = "Тепловой насос", TypeDescription = "Воздушные и геотермальные" },
                    new ClimateTechType { TypeName = "Увлажнитель", TypeDescription = "Увлажнители и очистители воздуха" }
                };
                await context.ClimateTechTypes.AddRangeAsync(types);
                await context.SaveChangesAsync();
            }

            // Добавляем тестовых пользователей
            if (!await context.Users.AnyAsync())
            {
                var users = new[]
                {
                    new User { Fio = "Иванов Иван Иванович", Phone = "+7 (999) 123-45-67", Login = "client", Password = "client", Type = "Заказчик" },
                    new User { Fio = "Петров Петр Петрович", Phone = "+7 (999) 234-56-78", Login = "master", Password = "master", Type = "Специалист" },
                    new User { Fio = "Сидоров Сидор Сидорович", Phone = "+7 (999) 345-67-89", Login = "manager", Password = "manager", Type = "Менеджер по качеству" }
                };
                await context.Users.AddRangeAsync(users);
                await context.SaveChangesAsync();
            }

            // Добавляем тестовые заявки
            if (!await context.Requests.AnyAsync())
            {
                var client = await context.Users.FirstOrDefaultAsync(u => u.Login == "client");
                var master = await context.Users.FirstOrDefaultAsync(u => u.Login == "master");
                var acType = await context.ClimateTechTypes.FirstOrDefaultAsync(t => t.TypeName == "Кондиционер");
                var newStatus = await context.RequestStatuses.FirstOrDefaultAsync(s => s.StatusName == "Новая заявка");
                var inProgressStatus = await context.RequestStatuses.FirstOrDefaultAsync(s => s.StatusName == "В процессе ремонта");

                if (client != null && acType != null && newStatus != null)
                {
                    var requests = new[]
                    {
                        new Request
                        {
                            StartDate = DateTime.Now.AddDays(-5),
                            TypeId = acType.TypeId,
                            Model = "Samsung AC123",
                            ProblemDescription = "Не охлаждает, компрессор шумит",
                            StatusId = newStatus.StatusId,
                            ClientId = client.UserId,
                            MasterId = master?.UserId
                        },
                        new Request
                        {
                            StartDate = DateTime.Now.AddDays(-3),
                            TypeId = acType.TypeId,
                            Model = "LG CoolPlus",
                            ProblemDescription = "Не включается, нет питания",
                            StatusId = inProgressStatus?.StatusId ?? newStatus.StatusId,
                            ClientId = client.UserId,
                            MasterId = master?.UserId
                        }
                    };
                    await context.Requests.AddRangeAsync(requests);
                    await context.SaveChangesAsync();
                }
            }
        }
    }
}