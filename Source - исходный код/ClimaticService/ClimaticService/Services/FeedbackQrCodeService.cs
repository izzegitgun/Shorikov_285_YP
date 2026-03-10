using QRCoder;

namespace ClimaticService.Services
{
    /// <summary>Сервис генерации QR-кода для оценки качества работы сервисной службы.</summary>
    public class FeedbackQrCodeService
    {
        // Ссылка на форму опроса качества для 3-го модуля
        private const string FeedbackFormUrl =
            "https://docs.google.com/forms/d/e/1FAIpQLSdhZcExx6LSIXxk0ub55mSu-WIh23WYdGG9HY5EZhLDo7P8eA/viewform?usp=sf_link";

        /// <summary>
        /// Генерирует PNG-изображение QR-кода как массив байт.
        /// </summary>
        public byte[] GenerateFeedbackQrCode(int? requestId = null)
        {
            // При необходимости можно добавлять идентификатор заявки в параметры формы
            var url = FeedbackFormUrl;

            using var qrGenerator = new QRCodeGenerator();
            using var qrCodeData = qrGenerator.CreateQrCode(url, QRCodeGenerator.ECCLevel.Q);
            var qrCode = new PngByteQRCode(qrCodeData);

            return qrCode.GetGraphic(20);
        }
    }
}

