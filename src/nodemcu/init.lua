-- The state is used to synchronize all the backend call
-- and sensor readings and alarms which allows a unified
-- approach of handling the state
local state = {
  backend_call = "",
  alarm = {
    sunset = false,
    sunrise = false,
    sunset_triggered = false,
    sunrise_triggered = false
  },
  request = {
    manual = {
      pattern_save = 'enabled',
      window_open = 'open'
    },
    data = {
      type = 'temperature',
      last = 'minute'
    },
    alarm = 'sunset'
  },
  auto_smart_mode = true,
  window_open = true,
  temperature = 33,
  humidity = 14,
  air_quality = 0,
  timer = {
    smart_mode = 5000,
    sensor_reading = 12000
  },
  alternate_read = 1,
  gas_enabled = true
}


-- the backend is primarily the serverside running on the
-- external computer. If the nodeMCU cannot connect to
-- the external server, blue light will appear.
local backend_call = {
  BASE_URL = 'http://192.168.0.15',
  APP = 'smartwindow',
  VERSION = 'v1',
  TYPE = {               -- types of call available
    TRAIN = 'train',     -- train a new predictive model
    RESET = 'reset',     -- reset the predictive model
    MANUAL = 'manual',   -- store data for machine learning
    AUTO = 'auto',       -- predict the window should open or close
    ALARM = 'alarm',     -- get the number of seconds left for specific task
    DATA = 'data'        -- get the weather data from third party providers
  }
}


-- Checks the internal nodeMCU state (line 4) and
-- decides whether the lights should open or closed
-- the function design allows to be triggered anywhere
-- because it reads the global state.
function updateLED()
  if(state.window_open == true) then
    pwm.setduty(3,1000)
    pwm.setduty(1,0)
  else
    pwm.setduty(3,0)
    pwm.setduty(1,1000)
  end
end


-- Some actions have a inherit delay because it required data to be
-- send from the server over the network and takes time. NodeMCU
-- needs to wait and then execute the perform_delayed_action
-- which uses the unified state to know what to do.
-- PARAMS: call_type (string) (backend call, line 40) and 
--         data (string) (data coming from backend)
local function perform_delayed_action(call_type, data)

  -- NodeMCU receives the seconds left for sunrise and sets
  -- an alarm. The alarm can be deactivated through the state.
  if(call_type == backend_call.TYPE.ALARM and
     state.request.alarm == 'sunrise' and
     not state.alarm.sunrise_triggered) then

    print("sunrise alarm setup")

    local start_timer = tmr.create()
    local time = tonumber(data)
    state.alarm.sunrise_triggered = true

    start_timer:register(time, tmr.ALARM_SINGLE, function()
      if(state.alarm.sunrise == true) then
        state.window_open = true
        state.alarm.sunrise_triggered = false
        state.request.manual.window_open = 'open'
        updateLED()
      end
    end)

    start_timer:start()

  -- NodeMCU receives the seconds left for sunset and sets
  -- an alarm. The alarm can be deactivated through the state.
  elseif(call_type == backend_call.TYPE.ALARM and
         state.request.alarm == 'sunset' and
         not state.alarm.sunset_triggered) then

    print("sunset alarm setup")

    local start_timer = tmr.create()
    local time = tonumber(data)
    state.alarm.sunset_triggered = true

    start_timer:register(time, tmr.ALARM_SINGLE, function()
      if(state.alarm.sunset == true) then
        state.window_open = false
        state.alarm.sunset_triggered = false
        state.request.manual.window_open = 'close'
        updateLED()
      end
    end)

    start_timer:start()

  -- The user and or nodeMCU can trigger the predictive model
  -- The prediction is executed on the server and sent over the
  -- network to the nodeMCU.
  elseif(call_type == backend_call.TYPE.AUTO) then
    if(data == '0') then
      state.window_open = false
      state.request.manual.window_open = 'close'
    else
      state.window_open = true
      state.request.manual.window_open = 'open'
    end

    print("auto executed")

    updateLED()

  -- Sensor recovery failure, NodeMCU requests data to the server
  -- about the temperature and updates the internal state, making the
  -- 'smart window' even the sensor DHT11 fails to read data
  elseif(call_type == backend_call.TYPE.DATA and
         state.request.data.type == 'temperature') then

    local temperature = tonumber(data)
    state.temperature = temperature

    print("updated temperature from api call")

  -- Sensor recovery failure, NodeMCU requests data to the server
  -- about the humidity and updates the internal state, making the
  -- 'smart window' even the sensor DHT11 fails to read data
  elseif(call_type == backend_call.TYPE.DATA and
         state.request.data.type == 'humidity') then

    local humidity = tonumber(data)
    state.humidity = humidity

    print("updated humidity from api call")

  end

end


-- The url refers to the backend where nodeMCU will ask for data, predictions,
-- saving data for machine learning and get the alarm for sunset or sunrise.
-- To see the types, please check the backend_call variable on line 40
-- PARAMS: type (string) referers to: backend call, line 40
local function get_url_factory(type)
  local url = backend_call.BASE_URL .. '/'
  url = url .. backend_call.APP .. '/'
  url = url .. backend_call.VERSION .. '/'

  if(type == backend_call.TYPE.TRAIN or type == backend_call.TYPE.RESET) then
    url = url .. type .. '/' .. 'pattern'

  elseif(type == backend_call.TYPE.MANUAL) then
    url = url .. type .. '/'
    url = url .. 'patternSave=' .. state.request.manual.pattern_save .. '&'
    url = url .. 'windowOpen=' .. state.request.manual.window_open .. '&'
    url = url .. 'temperature=' .. state.temperature .. '&'
    url = url .. 'humidity=' .. state.humidity

  elseif(type == backend_call.TYPE.AUTO) then
    url = url .. type .. '/'
    url = url .. 'temperature=' .. state.temperature .. '&'
    url = url .. 'humidity=' .. state.humidity

  elseif(type == backend_call.TYPE.ALARM) then
    url = url .. type .. '/' .. state.request.alarm

  elseif(type == backend_call.TYPE.DATA) then
    url = url .. type .. '/'
    url = url .. 'type=' .. state.request.data.type .. '&'
    url = url .. 'last=' .. state.request.data.last
  end

  return url
end


-- NodeMCU connects to the backend will ask for data, predictions,
-- saving data for machine learning and get the alarm for sunset or sunrise.
-- Apart of requesting data, there is an additional functionality of using
-- the nodeMCU incorporated LED to blink when it sends and receive data 
-- from backend if the backend is not available, the incorporated blue
-- led is not going to turn off
-- PARAMS: call_type (string) referers to: backend call, line 40
local function fetch_smart_window(call_type)
  urlAPI = get_url_factory(call_type)
  gpio.mode(0, gpio.OUTPUT)
  gpio.write(0, gpio.LOW)

  http.get(urlAPI, nil, function(code, data)
    if (code < 0) then
      print("http request failed")
    else
      gpio.mode(0, gpio.INPUT)
      gpio.write(0, gpio.HIGH)
      print ("http response code:"..code)
      perform_delayed_action(call_type, data)
    end
  end)
end


-- The client uses REST calls over HTTP to connect with the 
-- nodeMCU and perform operations such as opening or closing windows, 
-- auto smart modes, etc. The function handles the request and trigers 
-- the necessary steps to fullfil the task commanded by the client.
-- PARAMS: sck (object) connection with client
--         data (string) request information coming from client
local function tcp_receiver_handler(sck, data)
  print(data)

  if(string.find(data, 'GET /OPEN_WINDOW')) then
    state.request.manual.window_open = 'open'
    state.window_open = true
    fetch_smart_window(backend_call.TYPE.MANUAL)
    updateLED()

  elseif(string.find(data, 'GET /CLOSE_WINDOW')) then
    state.request.manual.window_open = 'close'
    state.window_open = false
    fetch_smart_window(backend_call.TYPE.MANUAL)
    updateLED()

  elseif(string.find(data, 'GET /ENABLE_SMARTMODE')) then
    state.auto_smart_mode = true
    print("auto smartmode enabled")

  elseif(string.find(data, 'GET /DISABLE_SMARTMODE')) then
    state.auto_smart_mode = false
    print("auto smartmode disabled")

  elseif(string.find(data, 'GET /TRAIN_PATTERN')) then
    fetch_smart_window(backend_call.TYPE.TRAIN)

  elseif(string.find(data, 'GET /RESET_PATTERN')) then
    fetch_smart_window(backend_call.TYPE.RESET)

  elseif(string.find(data, 'GET /ENABLE_PATTERN_SAVE')) then
    state.request.manual.pattern_save = 'enabled'
    print("pattern save enabled")

  elseif(string.find(data, 'GET /DISABLE_PATTERN_SAVE')) then
    state.request.manual.pattern_save = 'disabled'
    print("pattern save disabled")

  elseif(string.find(data, 'GET /ENABLE_SUNSET')) then
    state.alarm.sunset = true
    state.request.alarm = 'sunset'
    fetch_smart_window(backend_call.TYPE.ALARM)
    print("sunset window close enabled")

  elseif(string.find(data, 'GET /DISABLE_SUNSET')) then
    state.alarm.sunset = false
    print("sunset window close disabled")

  elseif(string.find(data, 'GET /ENABLE_SUNRISE')) then
    state.alarm.sunrise = true
    state.request.alarm = 'sunrise'
    fetch_smart_window(backend_call.TYPE.ALARM)
    print("sunrise window opening enabled")
  
  elseif(string.find(data, 'GET /DISABLE_SUNRISE')) then
    state.alarm.sunrise = false
    print("sunrise window opening disabled")

  elseif(string.find(data, 'GET /PREDICT_OPERATION')) then
    fetch_smart_window(backend_call.TYPE.AUTO)

  elseif(string.find(data, 'GET /ENABLE_GAS')) then
    state.gas_enabled = true
    print("enabled gas sensor")

  elseif(string.find(data, 'GET /DISABLE_GAS')) then
    state.gas_enabled = false
    print("disabled gas sensor")
  end

  sck:send("received")
  sck:on("sent", function(conn) conn:close() end)
end


-- The smart mode referes to the automated prediction whether the
-- window should be open or closed based on the temperature and
-- humidity. The request data is adquired through the state.
local function smart_mode()
  if(state.auto_smart_mode == true) then
    fetch_smart_window(backend_call.TYPE.AUTO)
  end
end


-- The timer allows nodeMCU to run the smart_mode automatically
-- and predict whether the window should be open on closed.
-- However, before requesting data to the backend the nodeMCU checks
-- the internal state and see if auto_smart_mode is enabled by the user.
local function set_timer_for_smartmode()
  local start_timer = tmr.create()
  start_timer:register(state.timer.smart_mode, 1, smart_mode)
  start_timer:start()
end


-- The sensor DHT11 does not allow to read the sensor values at the same
-- time. Thus, a semaphore is implemented to read one value a time. Given
-- the scenario (house) is not required to read both, temperature and humidity
-- at the same time.
-- PARAMS: mode (number) can be 1 for temperature and 2 for humidity
local function read_dht11(mode)
  local status, temp, humi, temp_dec, humi_dec = dht.read11(2)
  if status == dht.OK then
    if(mode == 1) then
      local value = tonumber(temp)
      state.temperature = value
      print("READ TEMP:" .. state.temperature)
    else
      local value = tonumber(humi)
      state.humidity = humi
      print("READ HUM:" .. state.humidity)
    end
    return true
  end
  return false
end


-- Due to the low cost of the sensors and nodeMCU and the inhability of
-- reading the sensors too quick which may also produce a race condition,
-- a semaphore is created to read one sensor value at a time.
-- Semaphore 1: temperature
-- Semaphore 2: humidity
-- Semaphore 3: Gas sensor
local function sensor_reading()
  if(state.alternate_read == 1) then
    if(read_dht11(1) == false) then
      state.request.data.type = 'temperature'
      fetch_smart_window(backend_call.TYPE.DATA)
    end
    state.alternate_read = 2
  elseif(state.alternate_read == 2) then
    if(read_dht11(2) == false) then
      state.request.data.type = 'humidity'
      fetch_smart_window(backend_call.TYPE.DATA)
    end
    state.alternate_read = 3
  else
    local quality = (tonumber(adc.read(0))/1024.0) * 100.0
    state.air_quality = quality
    state.alternate_read = 1
    print("READ AIR QUALITY: ".. state.air_quality)

    if(state.gas_enabled == true and state.air_quality > 50) then
      state.window_open = true
      updateLED()
    end
  end
end


local function set_timer_sensor_reading()
  local start_timer = tmr.create()
  start_timer:register(state.timer.sensor_reading, 1, sensor_reading)
  start_timer:start()
end


local function set_up_tcp_server_listen(conn)
  conn:on("receive", tcp_receiver_handler)
end

local start_timer = tmr.create()

start_timer:register(5000, tmr.ALARM_SINGLE, function()
  wifi.setmode(wifi.STATION)
  wifi.sta.config({ ssid = "VM9646364", pwd = "6zsmygSJdcd7" })

  wifi.sta.connect()
  wifi.eventmon.register(wifi.eventmon.STA_GOT_IP, function() 
    print("ip: " .. wifi.sta.getip())

    pwm.setup(3,1000,1023)   -- initialise the LEDs
    pwm.start(3)
    pwm.setup(1,1000,1023)
    pwm.start(1)
    updateLED()              -- update the LEDs based on the current state

    set_timer_for_smartmode()
    set_timer_sensor_reading()

    local tcp_server = net.createServer(net.TCP)
    tcp_server:listen(80, set_up_tcp_server_listen)
  end)
end)


start_timer:start()
