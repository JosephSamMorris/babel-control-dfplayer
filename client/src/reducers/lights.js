/*
The light array is arranged physically like this:
Adams St (west)
--O-O-O-O-O-O-O-O-O-O-O-O-O-- 0
--O-O-O-O-O-O-O-O-O-O-O-O-O-- 1
--O-O-O-O-O-O-O-O-O-O-O-O-O-- 2
--O-O-O-O-O-O-O-O-O-O-O-O-O-- 3
--O-O-O-O-O-O-O-O-O-O-O-O-O-- 4
--O-O-O-O-O-O-O-O-O-O-O-O-O-- 5
------O-O-O-O-O-O-O-O-O-O-O-- 6
------O-O-O-O-O-O-O-O-O-O-O-- 7
--O-O-O-O-O-O-O-O-O-O-O-O-O-- 8
--O-O-O-O-O-O-O-O-O-O-O-O-O-- 9
--O-O-O-O-O-O-O-O-O-O-O-O-O-- 10
--O-O-O-O-O-O-O-O-O-O-O-O-O-- 11
--O-O-O-O-O-O-O-O-O-O-O-O-O-- 12
--O-O-O-O-O-O-O-O-O-O-O-O-O-- 13
Anchorage Pl (east)
 */
function lightOffset(strand, position) {
  if (strand < 0 || strand >= 14) {
    throw new Error('Strand index must be between 0 and 13');
  }

  if (position < 0) {
    throw new Error('Position index must be between 0 and 13');
  }

  if ((strand < 6 || strand >= 8) && position > 13) {
    throw new Error('Position index must be between 0 and 13');
  }

  if ((strand === 6 || strand === 7) && position > 11) {
    throw new Error('Position index must be between 0 and 11 for the middle two strands');
  }
}

export default function lightsReducer(state, action) {
  if (state === undefined) {
    return {};
  }

  switch (action.type) {
    default:
      return state;
  }
}
