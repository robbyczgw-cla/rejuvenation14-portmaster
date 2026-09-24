# ROCKNIX/aarch64 compatibility preload for Rejuvenation V14.
# Runs before Data/Scripts.rxdata. Keeps the game folder untouched.

# 1. Stub libraries (discord.rb) take precedence over the x86_64 gems/discord.so.
PORT_RUBYLIB = File.expand_path("../rubylib", File.dirname(__FILE__))
$:.unshift(PORT_RUBYLIB) unless $:.include?(PORT_RUBYLIB)

# 2. Handheld has no windows. V14's Screen Size option (SpriteResizer.rb,
#    pbSetResizeFactor) switches to windowed mode and sets a window scale,
#    which fights the compositor and leaves stale frames at two scales
#    (menus drawn twice).
#    Keep mkxp-z in its own fullscreen mode (same as the game's
#    "Fullscreen" setting); scale/center only affect windows, so skip them.
module Graphics
  class << self
    alias_method :__port_set_fullscreen, :fullscreen=
    def fullscreen=(_value)
      __port_set_fullscreen(true)
    end

    def scale=(_value); end
    def center; end
  end
end

# 3. Handhelds have no keyboard. V14 defaults "Use Keyboard" to On
#    (Options.rb, PokemonOptions#fixMissingValues), which makes name entry
#    impossible with a pad. Default it to Off (character grid) for NEW
#    settings only; Settings.dat loaded from disk (Marshal) skips initialize,
#    so an explicit choice in the Options menu is kept.
module PortHandheldOptionDefaults
  def initialize(*args)
    @keyboard = 1 if @keyboard.nil?
    super
  end
end
$port_options_hook = TracePoint.new(:class) do |tp|
  if tp.self.name == "PokemonOptions"
    tp.self.prepend(PortHandheldOptionDefaults)
    $port_options_hook.disable
  end
end
$port_options_hook.enable
