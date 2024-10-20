import { set } from 'lodash';
import { useState } from 'react';
import { SlArrowRight, SlArrowLeft } from "react-icons/sl";

export default function Footer({ step, time, setTime }) {

  const [disabled, setDisabled] = useState(false)

  return (
    <>
      <div className='flex justify-center items-center absolute w-[calc(100%-418px)] h-32 right-0 bottom-0'>
        <div className='flex rounded-lg overflow-hidden shadow-xl'>
          <button className='bg-white h-full p-6'>
            <SlArrowLeft />
          </button>
          <div className='bg-red-800 px-8 text-center py-1'>
            <div className='text-white font-semibold text-xl'>
              {time % 24}:00
            </div>
            <div className='text-white'>
              Day {parseInt(time / 24)}
            </div>
          </div>
          <button className='bg-white h-full p-6' disabled={disabled} onClick={() => {
            setDisabled(true)
            setTimeout(() => {
              setDisabled(false)
            }, 2000)
            step()
          }}>
            <SlArrowRight />
          </button>
        </div>
      </div>
    </>
  )
}