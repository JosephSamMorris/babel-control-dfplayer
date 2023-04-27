import React, {useCallback, useEffect, useState} from 'react';
import styled from 'styled-components';

function OnOffButton({ className }) {
  const [isOn, setOn] = useState(undefined);

  useEffect(() => {
    fetch('/active')
      .then((res) => res.json())
      .then((on) => setOn(on));
  }, []);

  const handleClick = useCallback(() => {
    // Toggle state

    if (isOn) {
      fetch('/active', {
        method: 'POST',
        headers: {
          Accept: 'application/json',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ active: false }),
      })
        .then((res) => res.json())
        .then((on) => setOn(on));
    } else {
      fetch('/active', {
        method: 'POST',
        headers: {
          Accept: 'application/json',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ active: true }),
      })
        .then((res) => res.json())
        .then((on) => setOn(on));
    }
  }, [isOn]);

  return (
    <button disabled={isOn === undefined} className={className} onClick={handleClick} type="button">
      {isOn ? 'Turn Off' : 'Turn On'}
    </button>
  );
}

const StyledOnOffButton = styled(OnOffButton)`
  width: 100px;
  height: 100px;
`;

export default StyledOnOffButton;
