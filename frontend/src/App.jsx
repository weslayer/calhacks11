import { useState, useEffect, useRef } from 'react';
import Map from './Map';
import Marker from './Marker';
import Sidebar from './Sidebar';
import Footer from './Footer';
import './App.css';
import _, { initial } from 'lodash'
import 'date-fns'
import { getAgents, stepAgents } from './services/agent';

// Easing function (ease-in-out)
function easeInOut(t) {
    return t < 0.5 ? 4 * t * t * t : (t - 1) * (2 * t - 2) * (2 * t - 2) + 1;
}

function App() {
    const [markers, setMarkers] = useState([]);
    const [isAnimating, setIsAnimating] = useState(false);
    const animationRef = useRef(null);

    const [time, setTime] = useState(12);

    useEffect(() => {
        const interval = setInterval(async () => {
            const newAgents = await getAgents();
            setMarkers(newAgents.agents.map(agent => {
                return {
                    name: agent.name,
                    color: agent.infected ? 'red' : 'white',
                    latitude: agent.coordinates[0],
                    longitude: agent.coordinates[1],
                }
            }))
        }, 1000)

        return () => {
            clearInterval(interval)
        }
    }, [])

    const stepForward = _.throttle(() => {
        setTime(time + 1)
        stepAgents(`${time % 24}:00`)
    }, 2000)

    const animateMarkers = (initialMarker, nextMarker, startTime, duration) => {
        if (initialMarker.length === 0) {
            console.log(nextMarker)
            setMarkers(nextMarker)
        }

        const animate = (currentTime) => {
            const elapsedTime = currentTime - startTime;
            const rawProgress = Math.min(elapsedTime / duration, 1);
            const easedProgress = easeInOut(rawProgress);

            setMarkers(prevMarkers =>
                prevMarkers.map((marker, index) => {
                    const startPos = initialMarker[index];
                    const endPos = nextMarker[index];

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

    return (
        <>
            <Map>
                {markers.map((marker, index) => (
                    <Marker key={index} {...marker} />
                ))}
            </Map>
            <Sidebar />
            <Footer step={stepForward} time={time} setTime={setTime} />
        </>
    );
}

export default App;