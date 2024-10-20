import { SlArrowRight, SlArrowLeft } from "react-icons/sl";

export default function Footer() {
  return (
    <>
      <div className='flex justify-center items-center absolute w-[calc(100%-418px)] h-32 right-0 bottom-0'>
        <div className='flex rounded-lg overflow-hidden shadow-xl'>
          <button className='bg-white h-full p-6'>
            <SlArrowLeft />
          </button>
          <div className='bg-red-800 px-8 text-center py-1'>
            <div className='text-white font-semibold text-xl'>
              12:00 am
            </div>
            <div className='text-white'>
              Day 1
            </div>
          </div>
          <button className='bg-white h-full p-6'>
            <SlArrowRight />
          </button>
        </div>
      </div>
    </>
  )
}