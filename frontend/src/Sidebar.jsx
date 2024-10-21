import React, { useState } from 'react';
import './Sidebar.css';
import { SlArrowLeft, SlArrowRight } from 'react-icons/sl'
import { addContext } from './services/agent';

function Sidebar() {
  const [isOpen, setIsOpen] = useState(true);
  const [text, setText] = useState('');

  const toggleSidebar = () => {
    setIsOpen(!isOpen);
  };

  return (
    <div className={`${isOpen ? 'translate-x-0' : 'translate-x-[-390px]'} absolute top-0 left-0 h-full bg-red-800 w-[400px] white p-6 transition-transform ease-in-out duration-300 shadow-xl`}>
      <button className="text-white absolute top-0 right-[-18px] h-full bg-red-800 white border-none p-[5px] cursor-pointer" onClick={toggleSidebar}>
        {isOpen ? <SlArrowLeft /> : <SlArrowRight />}
      </button>
      <div className='text-white flex flex-col justify-between h-full'>
        <div className='text-white flex flex-col gap-4'>
          <div>
            <div className='text-white text-[70px] font-semibold tracking-[-5px]'><span className='text-orange-300'>INFER</span>mary</div>
            <div className='text-white text-sm'>viral spread simulator</div>
          </div>
          <div className="text-white flex justify-between border-b-2">
            <input className='text-orange-300 font-semibold text-[30px] w-[250px] tracking-tight bg-transparent' value={'San Francisco'} />
            <button>change city</button>
          </div>
          <div className="flex flex-col text-white gap-4">
            <div className='flex flex-col gap-1'>
              <span className='text-white font-bold text-xl'>Population:</span>
              <div className='text-md'>788,478</div>
            </div>
            <div className='flex flex-col gap-1'>
              <div className='text-white font-bold text-xl'>Population Density:</div>
              <div className='text-md'>18,633 per square mile</div>
            </div>
            <div className='flex flex-col gap-1'>
              <div className='text-white font-bold text-xl'>Land Area:</div>
              <div className='text-md'>46.87 square miles</div>
            </div>
          </div>
        </div>
        <div className='flex flex-col gap-8'>
          <div className='flex flex-col gap-4'>
            <div className="text-orange-300 font-semibold text-[30px] tracking-tight border-b-2">Simulation Parameters</div>
            <div className='text-md flex justify-between'>
              <div className='flex-1'>Virus Reproduction Chance:</div>
              <input style={{ width: 50 }} className='border-b-2 bg-transparent text-right' type="number" value="3" />
            </div>
            <div className='text-md flex justify-between'>
              Number of Initial Infected:
              <input style={{ width: 50 }} className='border-b-2 bg-transparent text-right' type="number" value="15" />
            </div>
          </div>
          <div className="flex flex-col text-white section gap-4">
            <div className='text-orange-300 font-semibold text-[30px] tracking-tight border-b-2'>Other Factors</div>
            <textarea className='w-full p-2 text-red-800 rounded-md' placeholder="Describe any other factors in plain text..." value={text} onChange={(e) => setText(e.target.value)}></textarea>
          </div>
          <button className="begin-button" onClick={() => {
            addContext(text)
            setText('')
          }}>Add Context</button>
        </div>
      </div>
    </div>
  );
}

export default Sidebar;