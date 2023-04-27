import React, {useCallback, useEffect, useState} from 'react';
import styled from 'styled-components';
import PropTypes from 'prop-types';
import {ProviderProps} from 'react-redux/es/exports';

function LightStatus({ className, brightness, volume }) {
  if (brightness < 0 || brightness > 1) {
    throw new Error('Brightness must be 0-1');
  }

  if (volume < 0 || volume > 1) {
    throw new Error('Volume must be 0-1');
  }

  const width = 100;
  const height = width;
  const strokeWidth = 4;

  const radius = width / 2;

  const cx = width / 2;
  const cy = height / 2;

  const colorVal = Math.floor(brightness * 255);
  const lightColor = `rgb(${colorVal}, ${colorVal}, ${colorVal})`;
  const volumeRadius = radius * 0.5;

  return (
    <svg className={className} viewBox={`0 0 ${width} ${height}`}>
      <circle className="outline" cx={cx} cy={cy} r={radius - strokeWidth / 2} />
      <circle className="light" fill={lightColor} cx={cx} cy={cy} r={radius - strokeWidth / 2} />
      <circle className="volume-outline" cx={cx} cy={cy} r={volumeRadius} />
      <circle className="volume" cx={cx} cy={cy} r={volumeRadius * volume} />
    </svg>
  );
}

LightStatus.propTypes = {
  className: PropTypes.string,
  brightness: PropTypes.number,
  volume: PropTypes.number,
};

LightStatus.defaultProps = {
  className: undefined,
  brightness: 0,
  volume: 0,
};

const StyledLightStatus = styled(LightStatus)`
  width: 500px;
  height: 500px;
  stroke-width: 4px;

  .outline {
    stroke: black;
    fill: none;
  }
  
  .light {
    stroke: none;
  }
  
  .volume-outline {
    stroke: white;
    fill: white;
  }
  
  .volume {
    stroke: none;
    fill: black;
  }
`;

export default StyledLightStatus;
