#include <stdint.h>
#include <math.h>

void grayscale_vignette(uint8_t *image, int width, int height) {
    int center_x = width / 2;
    int center_y = height / 2;
    float max_dist = sqrt(center_x * center_x + center_y * center_y);

    for (int y = 0; y < height; ++y) {
        for (int x = 0; x < width; ++x) {
            int i = (y * width + x) * 3;

            uint8_t r = image[i];
            uint8_t g = image[i + 1];
            uint8_t b = image[i + 2];
            uint8_t gray = (r + g + b) / 3;

            float dx = x - center_x;
            float dy = y - center_y;
            float dist = sqrt(dx * dx + dy * dy);
            float factor = 1.0f - (dist / max_dist);
            if (factor < 0.0f) factor = 0.0f;

            uint8_t result = (uint8_t)(gray * factor);
            image[i] = image[i + 1] = image[i + 2] = result;
        }
    }
}
