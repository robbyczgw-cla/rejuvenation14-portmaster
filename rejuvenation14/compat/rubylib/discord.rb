# Stand-in for gems/discord.so (x86_64 Discord Game SDK binding).
# Rejuvenation only uses it for rich presence; gameplay does not need it.
module Discord
  module_function

  def update; end
  def connected?; false; end
  def connect(*); false; end
  def disconnect; end
  def update_activity(*); end
  def clear_activity(*); end

  def method_missing(*) = nil
  def respond_to_missing?(*) = true
end
