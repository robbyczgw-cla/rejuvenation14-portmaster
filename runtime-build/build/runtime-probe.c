#include <SDL.h>
#include <stdio.h>

int main(void) {
    SDL_version v;
    SDL_GetVersion(&v);
    printf("SDL %d.%d.%d\n", v.major, v.minor, v.patch);
    for (int i = 0; i < SDL_GetNumVideoDrivers(); ++i)
        printf("video: %s\n", SDL_GetVideoDriver(i));
    for (int i = 0; i < SDL_GetNumAudioDrivers(); ++i)
        printf("audio: %s\n", SDL_GetAudioDriver(i));
    printf("No SDL_Init, window, audio device, or controller opened.\n");
    return 0;
}
