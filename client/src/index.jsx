import React from 'react';
import * as ReactDOM from 'react-dom/client';
import { createStore } from 'redux';
import { Provider } from 'react-redux';
import styled, { createGlobalStyle } from 'styled-components';

import rootReducer from './reducers';

import ArrayDiagram from './components/ArrayDiagram';
import FilterSection from './components/FilterSection';
import ControlSection from './components/ControlSection';
import LightPanel from './components/LightPanel';
import InventorySection from './components/InventorySection';
import LightStatus from './components/LightStatus';
import OnOffButton from './components/OnOffButton';

const store = createStore(rootReducer);

const GlobalStyle = createGlobalStyle`
  body {
    margin: 0;
  }
`;

const Wrapper = styled.div`
  display: flex;
  flex-direction: column;
`;

const ButtonWrapper = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 100px;
`;

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <Provider store={store}>
    <GlobalStyle />
    <ButtonWrapper>
      <OnOffButton />
    </ButtonWrapper>
  </Provider>,
);
