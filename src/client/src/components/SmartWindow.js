import { fetch_nodemcu } from '../api/request'
import style from './smartwindow.module.css'

// the call_type is coming from the nodeMCU list of
// available request to trigger the nodeMCU to perform
// an action
const smart_window_features = [
  {
    title: 'Open window',
    call_type: 'OPEN_WINDOW'
  },
  {
    title: 'Close window',
    call_type: 'CLOSE_WINDOW'
  },
  {
    title: 'Trigger automated action',
    call_type: 'PREDICT_OPERATION'
  },
  {
    title: 'Enable close window on sunset',
    call_type: 'ENABLE_SUNSET'
  },
  {
    title: 'Disable close window on sunset',
    call_type: 'DISABLE_SUNSET'
  },
  {
    title: 'Enable open window on sunrise',
    call_type: 'ENABLE_SUNRISE'
  },
  {
    title: 'Disable open window on sunrise',
    call_type: 'DISABLE_SUNRISE'
  },
  {
    title: 'Enable gas detection',
    call_type: 'ENABLE_GAS'
  },
  {
    title: 'Disable gas detection',
    call_type: 'DISABLE_GAS'
  }
]

// the call_type is coming from the nodeMCU list of
// available request to trigger the nodeMCU to perform
// an action
const smart_window_advanced_settings = [
  {
    title: 'Train new predictive model',
    call_type: 'TRAIN_PATTERN'
  },
  {
    title: 'Reset predictive model',
    call_type: 'RESET_PATTERN'
  },
  {
    title: 'Enable auto smartmode',
    call_type: 'ENABLE_SMARTMODE'
  },
  {
    title: 'Disable auto smartmode',
    call_type: 'DISABLE_SMARTMODE'
  },
  {
    title: 'Enable pattern save',
    call_type: 'ENABLE_PATTERN_SAVE'
  },
  {
    title: 'Disable pattern save',
    call_type: 'DISABLE_PATTERN_SAVE'
  }
]

const Box = ({ title, call_type, click = 'execute' }) => (
  <div className={style.box}>
    <p>{title}</p>
    <button onClick={() => { fetch_nodemcu(call_type) }}>
      {click}
    </button>
  </div>
)


function SmartWindow() {
  return (
    <>
      <h1>Smart Window Control Panel</h1>
      <div className={style.boxarea}>
        <b>Features</b>
        <div className={style.boxoptions}>
          {smart_window_features.map(
            feature => <Box title={feature.title} call_type={feature.call_type}/>
          )}
        </div>
      </div>
      <div className={style.boxarea}>
        <b>Advanced Settings</b>
        <div className={style.boxoptions}>
          {smart_window_advanced_settings.map(
            feature => <Box title={feature.title} call_type={feature.call_type}/>
          )}
        </div>
      </div>
    </>
  );
}


export default SmartWindow;
