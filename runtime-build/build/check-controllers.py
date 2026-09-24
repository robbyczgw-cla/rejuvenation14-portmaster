"""Exercise the patched event handlers with virtual SDL pads, without video."""
from pathlib import Path
import shlex
import subprocess

source = Path('/work/source/src/eventthread.cpp').read_text()
opening = source[source.index('    std::map<SDL_JoystickID'):source.index('    char buffer[128];')]
handlers = source[source.index('            case SDL_CONTROLLERBUTTONDOWN:'):source.index('            case SDL_MOUSEBUTTONDOWN :', source.index('            case SDL_CONTROLLERBUTTONDOWN:'))]
cleanup_start = source.index('    for (const auto &controller : controllers)')
cleanup = source[cleanup_start:source.index('#ifndef MKXPZ_BUILD_XCODE', cleanup_start)]
program = r'''
#include <SDL.h>
#include <cassert>
#include <cmath>
#include <cstdio>
#include <cstring>
#include <map>
struct Flag { void clear() {} void set() {} };
int main() {
    assert(SDL_Init(SDL_INIT_GAMECONTROLLER) == 0);
    // Index zero is deliberately not a game controller.
    assert(SDL_JoystickAttachVirtual(SDL_JOYSTICK_TYPE_FLIGHT_STICK, 2, 2, 0) == 0);
    assert(SDL_JoystickAttachVirtual(SDL_JOYSTICK_TYPE_GAMECONTROLLER, SDL_CONTROLLER_AXIS_MAX, SDL_CONTROLLER_BUTTON_MAX, 0) == 1);
    assert(SDL_JoystickAttachVirtual(SDL_JOYSTICK_TYPE_GAMECONTROLLER, SDL_CONTROLLER_AXIS_MAX, SDL_CONTROLLER_BUTTON_MAX, 0) == 2);
    SDL_GameController *ctrl = nullptr;
''' + opening + r'''
    assert(controllers.size() == 2);
    auto first = controllers.begin()->second;
    auto second = controllers.rbegin()->second;
    auto firstId = controllers.begin()->first;
    auto secondId = controllers.rbegin()->first;
    assert(ctrl == first);
    struct { bool buttons[SDL_CONTROLLER_BUTTON_MAX]{}; int axes[SDL_CONTROLLER_AXIS_MAX]{}; } controllerState;
    struct { struct { bool enableReset = false; float axisDeadzone[SDL_CONTROLLER_AXIS_MAX]; } config; Flag rqResetFinish, rqReset; } rtData;
    for (auto &value : rtData.config.axisDeadzone) value = 0.2f;
    bool resetting = false;
    int lastInputDevice = 0, resetCount = 0;
    const int LAST_INPUT_DEVICE_GAMEPAD = 1;
    auto resetInputStates = [&]() { ++resetCount; memset(&controllerState, 0, sizeof(controllerState)); };
    auto dispatch = [&](SDL_Event event) {
        switch (event.type) {
''' + handlers + r'''
        }
    };
    auto drain = [&]() { SDL_Event event; SDL_PumpEvents(); while (SDL_PollEvent(&event)) dispatch(event); };
    drain(); // Startup ADDED events must not open a second reference.
    assert(controllers.size() == 2);
    auto press = [&](SDL_GameController *pad, int button, int value) {
        assert(SDL_JoystickSetVirtualButton(SDL_GameControllerGetJoystick(pad), button, value) == 0);
        drain();
    };
    press(second, SDL_CONTROLLER_BUTTON_A, 1);
    assert(ctrl == second && controllerState.buttons[SDL_CONTROLLER_BUTTON_A]);
    press(second, SDL_CONTROLLER_BUTTON_A, 0);
    assert(!controllerState.buttons[SDL_CONTROLLER_BUTTON_A]);
    press(first, SDL_CONTROLLER_BUTTON_B, 1);
    assert(ctrl == first && controllerState.buttons[SDL_CONTROLLER_BUTTON_B]);
    auto axis = [&](SDL_GameController *pad, int index, int value) {
        assert(SDL_JoystickSetVirtualAxis(SDL_GameControllerGetJoystick(pad), index, value) == 0);
        drain();
    };
    axis(first, SDL_CONTROLLER_AXIS_LEFTX, 20000);
    axis(first, SDL_CONTROLLER_AXIS_RIGHTY, -24000);
    for (int noise : {1000, -1000, 0, 6000, -6000}) {
        axis(second, SDL_CONTROLLER_AXIS_LEFTX, noise);
        assert(ctrl == first && controllerState.axes[SDL_CONTROLLER_AXIS_LEFTX] == 20000);
        assert(controllerState.axes[SDL_CONTROLLER_AXIS_RIGHTY] == -24000);
    }
    // The deadzone boundary is inclusive for inactive pads, in both directions.
    rtData.config.axisDeadzone[SDL_CONTROLLER_AXIS_LEFTX] = 1.0f;
    axis(second, SDL_CONTROLLER_AXIS_LEFTX, 32767);
    axis(second, SDL_CONTROLLER_AXIS_LEFTX, -32767);
    assert(ctrl == first && controllerState.axes[SDL_CONTROLLER_AXIS_LEFTX] == 20000);
    rtData.config.axisDeadzone[SDL_CONTROLLER_AXIS_LEFTX] = 0.2f;
    axis(second, SDL_CONTROLLER_AXIS_LEFTX, -20000);
    assert(ctrl == second && controllerState.axes[SDL_CONTROLLER_AXIS_LEFTX] == -20000);
    assert(controllerState.axes[SDL_CONTROLLER_AXIS_RIGHTY] == 0);
    assert(controllerState.buttons[SDL_CONTROLLER_BUTTON_B]);
    // Returning the primary stick to neutral must still update shared axes.
    axis(second, SDL_CONTROLLER_AXIS_LEFTX, -1000);
    assert(ctrl == second && controllerState.axes[SDL_CONTROLLER_AXIS_LEFTX] == -1000);
    axis(second, SDL_CONTROLLER_AXIS_LEFTX, 0);
    assert(controllerState.axes[SDL_CONTROLLER_AXIS_LEFTX] == 0);
    axis(second, SDL_CONTROLLER_AXIS_LEFTY, 18000);
    press(second, SDL_CONTROLLER_BUTTON_A, 1);
    assert(controllerState.axes[SDL_CONTROLLER_AXIS_LEFTY] == 18000);
    press(first, SDL_CONTROLLER_BUTTON_X, 1);
    assert(ctrl == first);
    for (int value : controllerState.axes) assert(value == 0);
    assert(controllerState.buttons[SDL_CONTROLLER_BUTTON_A]);
    assert(controllerState.buttons[SDL_CONTROLLER_BUTTON_B]);
    assert(controllerState.buttons[SDL_CONTROLLER_BUTTON_X]);
    // Old-primary noise must not disturb a new primary after a button switch.
    axis(first, SDL_CONTROLLER_AXIS_RIGHTX, 23000);
    axis(second, SDL_CONTROLLER_AXIS_LEFTY, 500);
    assert(ctrl == first && controllerState.axes[SDL_CONTROLLER_AXIS_RIGHTX] == 23000);
    assert(controllerState.axes[SDL_CONTROLLER_AXIS_LEFTY] == 0);
    axis(second, SDL_CONTROLLER_AXIS_LEFTX, 20000);
    assert(ctrl == second && controllerState.axes[SDL_CONTROLLER_AXIS_LEFTX] == 20000);
    assert(controllerState.axes[SDL_CONTROLLER_AXIS_RIGHTX] == 0);
    press(second, SDL_CONTROLLER_BUTTON_GUIDE, 1);
    assert(!resetting && !controllerState.buttons[SDL_CONTROLLER_BUTTON_GUIDE]);
    press(second, SDL_CONTROLLER_BUTTON_GUIDE, 0);
    assert(!resetting);
    // Remove non-primary: preserve shared input, close exactly its handle.
    assert(SDL_JoystickDetachVirtual(1) == 0);
    drain();
    assert(controllers.size() == 1 && ctrl == second && resetCount == 0);
    // SDL itself emits button-up events when a virtual pad is detached.
    assert(SDL_GameControllerFromInstanceID(firstId) == nullptr);
    // Add another controller, then remove the primary and fall back to it.
    assert(SDL_JoystickAttachVirtual(SDL_JOYSTICK_TYPE_GAMECONTROLLER, SDL_CONTROLLER_AXIS_MAX, SDL_CONTROLLER_BUTTON_MAX, 0) == 2);
    drain();
    assert(controllers.size() == 2 && ctrl == second);
    assert(SDL_JoystickDetachVirtual(1) == 0);
    drain();
    assert(controllers.size() == 1 && ctrl && ctrl != second && resetCount == 1);
    assert(!controllerState.buttons[SDL_CONTROLLER_BUTTON_B]);
    assert(SDL_GameControllerFromInstanceID(secondId) == nullptr);
    SDL_Event unknown{}; unknown.type = SDL_CONTROLLERDEVICEREMOVED; unknown.cdevice.which = 123456;
    dispatch(unknown);
    assert(controllers.size() == 1 && resetCount == 1);
    assert(SDL_JoystickDetachVirtual(1) == 0);
    drain();
    assert(controllers.empty() && ctrl == nullptr && resetCount == 2);
    // Verify event-loop cleanup balances all opens, including startup rescans.
    assert(SDL_JoystickAttachVirtual(SDL_JOYSTICK_TYPE_GAMECONTROLLER, SDL_CONTROLLER_AXIS_MAX, SDL_CONTROLLER_BUTTON_MAX, 0) == 1);
    drain();
    auto finalId = controllers.begin()->first;
''' + cleanup + r'''
    assert(ctrl == nullptr && SDL_GameControllerFromInstanceID(finalId) == nullptr);
    SDL_Quit();
    puts("PASS: two virtual pads, non-controller index 0, startup rescans, inactive axis noise rejected including exact deadzone boundary, primary neutral accepted, axes cleared on button/axis primary switch, buttons preserved, Guide disabled, hotplug, exact close, primary-only reset, fallback, final cleanup");
}
'''
Path('/tmp/check-controllers.cpp').write_text(program)
flags = subprocess.check_output(['pkg-config', '--cflags', '--libs', '--static', 'sdl2'], text=True)
subprocess.run(['c++', '-std=c++11', '/tmp/check-controllers.cpp', '-o', '/tmp/check-controllers', *shlex.split(flags)], check=True)
subprocess.run(['/tmp/check-controllers'], check=True)
