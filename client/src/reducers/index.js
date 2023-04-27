import { combineReducers } from 'redux';
import lightsReducer from './lights';

export default combineReducers({
  lights: lightsReducer,
});
