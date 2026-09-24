require 'rbconfig'
%w[zlib fiddle openssl json bigdecimal date digest etc io/console io/nonblock io/wait
   nkf pathname psych racc/cparse socket stringio strscan syslog enc/encdb enc/trans/transdb].each do |name|
  require name
  puts "require #{name}: OK"
end
raise 'Ruby version mismatch' unless RUBY_VERSION == '3.1.3'
raise 'Ruby architecture mismatch' unless RUBY_PLATFORM == 'aarch64-linux'
text = 'Rejuvenation äöü'
raise 'zlib round trip' unless Zlib::Inflate.inflate(Zlib::Deflate.deflate(text)).b == text.b
raise 'JSON round trip' unless JSON.parse(JSON.generate({'test' => text}))['test'] == text
raise 'OpenSSL digest' unless OpenSSL::Digest::SHA256.hexdigest('abc') == 'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad'
strlen = Fiddle::Function.new(Fiddle::Handle::DEFAULT['strlen'], [Fiddle::TYPE_VOIDP], Fiddle::TYPE_SIZE_T)
raise 'libffi call' unless strlen.call('runtime') == 7
raise 'encoding round trip' unless text.encode('UTF-16LE').encode('UTF-8') == text
puts RUBY_DESCRIPTION
puts "RbConfig arch: #{RbConfig::CONFIG['arch']}"
puts OpenSSL::OPENSSL_VERSION
puts "Zlib #{Zlib::ZLIB_VERSION}; Fiddle #{Fiddle::VERSION}; JSON #{JSON::VERSION}"
puts 'Ruby native extension checks: PASS. No graphics or network connection opened.'
