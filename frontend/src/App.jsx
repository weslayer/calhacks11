import React, { useState, useEffect, useRef } from 'react';
import Map from './Map';
import Marker from './Marker';
import Sidebar from './Sidebar';
import './App.css';
import AnimatedCursor from "react-animated-cursor"

const initialMarkerData = [
  { longitude: -122.4194, latitude: 37.7749, color: "red" }, 
  { longitude: -122.4, latitude: 37.8, color: "red" }
];

const nextMarkerDest = [
  { longitude: -122.45, latitude: 37.75, color: "red" }, 
  { longitude: -122.41, latitude: 37.81, color: "red" }
];

// Easing function (ease-in-out)
function easeInOut(t) {
  return t < 0.5 ? 4 * t * t * t : (t - 1) * (2 * t - 2) * (2 * t - 2) + 1;
}

function App() {
  const [markers, setMarkers] = useState(initialMarkerData);
  const [isAnimating, setIsAnimating] = useState(false);
  const animationRef = useRef(null);

  const animateMarkers = (startTime, duration) => {
    const animate = (currentTime) => {
      const elapsedTime = currentTime - startTime;
      const rawProgress = Math.min(elapsedTime / duration, 1);
      const easedProgress = easeInOut(rawProgress);

      setMarkers(prevMarkers => 
        prevMarkers.map((marker, index) => {
          const startPos = initialMarkerData[index];
          const endPos = nextMarkerDest[index];
          
          return {
            ...marker,
            longitude: startPos.longitude + (endPos.longitude - startPos.longitude) * easedProgress,
            latitude: startPos.latitude + (endPos.latitude - startPos.latitude) * easedProgress,
          };
        })
      );

      if (rawProgress < 1) {
        animationRef.current = requestAnimationFrame((time) => animate(time));
      } else {
        setIsAnimating(false);
      }
    };

    animationRef.current = requestAnimationFrame((time) => animate(time));
  };

  useEffect(() => {
    // Start animation on component mount
    if (!isAnimating) {
      setIsAnimating(true);
      const animationDuration = 4000; // Duration in milliseconds
      animateMarkers(performance.now(), animationDuration);
    }

    // Cleanup function to cancel animation if the component unmounts
    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, []); 

  return (
    <>
    <AnimatedCursor 
    outerScale={1}
    trailingSpeed={1000000}
    />
      <Map>
        {markers.map((marker, index) => (
          <Marker key={index} {...marker} />
        ))}
      </Map>
      <Sidebar />
    </>
  );
}

export default App;