import React, { useState, useEffect } from 'react';
import { FileText, Link, Upload, Cpu, Sparkles, Network } from 'lucide-react';

const FuturisticInterface = () => {
  const [progress, setProgress] = useState(0);
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    const logMessages = [
      '正在解析数据模型...',
      '神经网络初始化中...',
      '正在读取语义信息...',
      '模型训练进度：47%',
      '优化参数配置...',
      '加载深度学习模型...'
    ];

    const interval = setInterval(() => {
      if (logs.length < logMessages.length) {
        setLogs(prev => [...prev, logMessages[prev.length]]);
        setProgress(prev => Math.min(prev + 15, 100));
      }
    }, 1500);

    return () => clearInterval(interval);
  }, [logs]);

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-950 to-purple-950 flex flex-col p-8 relative overflow-hidden">
      {/* Decorative Background Elements */}
      <div className="absolute inset-0 overflow-hidden">
        {/* Floating Icons */}
        {[...Array(6)].map((_, index) => (
          <div
            key={index}
            className="absolute text-blue-500/10"
            style={{
              left: `${Math.random() * 90}%`,
              top: `${Math.random() * 90}%`,
              transform: `rotate(${Math.random() * 360}deg)`,
              animation: `float ${5 + Math.random() * 5}s infinite ease-in-out`
            }}
          >
            {index % 3 === 0 && <Cpu size={96} />}
            {index % 3 === 1 && <Sparkles size={96} />}
            {index % 3 === 2 && <Network size={96} />}
          </div>
        ))}

        {/* Particles */}
        {[...Array(50)].map((_, i) => (
          <div
            key={i}
            className="absolute w-1 h-1 bg-blue-400 rounded-full opacity-20 animate-pulse"
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
              animationDelay: `${Math.random() * 2}s`,
              animationDuration: `${3 + Math.random() * 4}s`
            }}
          />
        ))}
      </div>

      {/* Header with Robot Avatar and Title */}
      <div className="relative z-10 flex items-center mb-16 justify-center">
        <div className="flex items-center gap-8">
          <div className="relative group">
            <div className="w-40 h-40 rounded-full bg-black p-1">
              <div className="w-full h-full rounded-full bg-black flex items-center justify-center overflow-hidden relative">
                <div className="absolute inset-0 bg-gradient-to-r from-green-500/20 via-green-500/10 to-green-500/20 animate-pulse"></div>
                <svg viewBox="0 0 200 200" className="w-full h-full">
                    <defs>
                        <linearGradient id="digitalRain" x1="0%" y1="0%" x2="0%" y2="100%">
                            <stop offset="0%" stopColor="#00ff00" stopOpacity="0.1"/>
                            <stop offset="50%" stopColor="#00ff00" stopOpacity="0.3"/>
                            <stop offset="100%" stopColor="#00ff00" stopOpacity="0.1"/>
                            <animate attributeName="y1" values="0%;100%;0%" dur="3s" repeatCount="indefinite"/>
                            <animate attributeName="y2" values="100%;200%;100%" dur="3s" repeatCount="indefinite"/>
                        </linearGradient>
                        <filter id="glow">
                            <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
                            <feMerge>
                                <feMergeNode in="coloredBlur"/>
                                <feMergeNode in="SourceGraphic"/>
                            </feMerge>
                        </filter>
                        <pattern id="matrix" x="0" y="0" width="20" height="20" patternUnits="userSpaceOnUse">
                            <text x="0" y="10" fill="#00ff00" opacity="0.3" fontFamily="monospace" fontSize="10">1</text>
                            <text x="10" y="15" fill="#00ff00" opacity="0.3" fontFamily="monospace" fontSize="10">0</text>
                        </pattern>
                    </defs>
                    
                    <rect x="0" y="0" width="200" height="200" fill="url(#matrix)" opacity="0.5">
                        <animate attributeName="opacity" values="0.3;0.6;0.3" dur="4s" repeatCount="indefinite"/>
                    </rect>
                    
                    <circle cx="100" cy="100" r="80" fill="none" stroke="#00ff00" strokeWidth="1" opacity="0.5">
                        <animate attributeName="r" values="75;85;75" dur="3s" repeatCount="indefinite"/>
                        <animate attributeName="stroke-opacity" values="0.3;0.8;0.3" dur="3s" repeatCount="indefinite"/>
                    </circle>
                    
                    <circle cx="100" cy="100" r="70" fill="url(#digitalRain)" opacity="0.3"/>
                    
                    {/* Left Eye */}
                    <g transform="translate(70,90)">
                        <ellipse rx="20" ry="12" 
                                fill="none" 
                                stroke="#00ff00" 
                                strokeWidth="1"
                                filter="url(#glow)">
                            <animate attributeName="ry" 
                                    values="12;2;12" 
                                    dur="4s" 
                                    repeatCount="indefinite"/>
                        </ellipse>
                        
                        <ellipse rx="15" ry="9" 
                                fill="none" 
                                stroke="#00ff00" 
                                strokeWidth="0.5" 
                                opacity="0.7"
                                filter="url(#glow)">
                            <animate attributeName="ry" 
                                    values="9;1;9" 
                                    dur="4s" 
                                    repeatCount="indefinite"/>
                        </ellipse>
                        
                        <circle r="4" 
                                fill="#00ff00" 
                                opacity="0.9"
                                filter="url(#glow)">
                            <animate attributeName="r" 
                                    values="4;2;4" 
                                    dur="4s" 
                                    repeatCount="indefinite"/>
                        </circle>
                    </g>

                    {/* Right Eye */}
                    <g transform="translate(130,90)">
                        <ellipse rx="20" ry="12" 
                                fill="none" 
                                stroke="#00ff00" 
                                strokeWidth="1"
                                filter="url(#glow)">
                            <animate attributeName="ry" 
                                    values="12;2;12" 
                                    dur="4s" 
                                    repeatCount="indefinite"/>
                        </ellipse>
                        
                        <ellipse rx="15" ry="9" 
                                fill="none" 
                                stroke="#00ff00" 
                                strokeWidth="0.5" 
                                opacity="0.7"
                                filter="url(#glow)">
                            <animate attributeName="ry" 
                                    values="9;1;9" 
                                    dur="4s" 
                                    repeatCount="indefinite"/>
                        </ellipse>
                        
                        <circle r="4" 
                                fill="#00ff00" 
                                opacity="0.9"
                                filter="url(#glow)">
                            <animate attributeName="r" 
                                    values="4;2;4" 
                                    dur="4s" 
                                    repeatCount="indefinite"/>
                        </circle>
                    </g>

                    {/* Connection between eyes */}
                    <path d="M 90 90 L 110 90" 
                          stroke="#00ff00" 
                          strokeWidth="0.5" 
                          opacity="0.5"
                          filter="url(#glow)">
                        <animate attributeName="opacity" 
                                values="0.2;0.8;0.2" 
                                dur="2s" 
                                repeatCount="indefinite"/>
                    </path>
                </svg>
              </div>
            </div>
            <div className="absolute -inset-2 bg-gradient-to-r from-green-500 to-green-500/50 rounded-full opacity-20 group-hover:opacity-30 blur transition-opacity"></div>
          </div>
          <div className="text-center">
            <h1 className="text-7xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 via-purple-400 to-cyan-400 tracking-tight">
              Tommy's AI Brain
            </h1>
            <p className="text-2xl text-blue-300 mt-4 font-light">Your Personal Knowledge Assistant</p>
          </div>
        </div>
      </div>

      <div className="relative z-10 flex-1 flex flex-col items-center justify-center max-w-2xl mx-auto w-full">
        {/* Main Buttons */}
        <div className="flex justify-center gap-6 mb-16 w-full">
          <button className="group flex flex-col items-center gap-3 p-6 bg-white/5 backdrop-blur-lg rounded-2xl hover:bg-white/10 transition-all duration-300 border border-blue-500/20">
            <div className="w-16 h-16 flex items-center justify-center rounded-full bg-blue-500/20 group-hover:bg-blue-500/30 transition-colors">
              <FileText className="w-8 h-8 text-blue-400" />
            </div>
            <span className="text-blue-200 font-medium">文本链接</span>
          </button>

          <button className="group flex flex-col items-center gap-3 p-6 bg-white/5 backdrop-blur-lg rounded-2xl hover:bg-white/10 transition-all duration-300 border border-purple-500/20">
            <div className="w-16 h-16 flex items-center justify-center rounded-full bg-purple-500/20 group-hover:bg-purple-500/30 transition-colors">
              <Link className="w-8 h-8 text-purple-400" />
            </div>
            <span className="text-purple-200 font-medium">音频链接</span>
          </button>

          <button className="group flex flex-col items-center gap-3 p-6 bg-white/5 backdrop-blur-lg rounded-2xl hover:bg-white/10 transition-all duration-300 border border-cyan-500/20">
            <div className="w-16 h-16 flex items-center justify-center rounded-full bg-cyan-500/20 group-hover:bg-cyan-500/30 transition-colors">
              <Upload className="w-8 h-8 text-cyan-400" />
            </div>
            <span className="text-cyan-200 font-medium">上传音频</span>
          </button>
        </div>

        {/* Progress Bar */}
        <div className="mb-8 w-full">
          <div className="h-2 bg-blue-950 rounded-full overflow-hidden">
            <div 
              className="h-full bg-gradient-to-r from-blue-500 via-purple-500 to-cyan-500 transition-all duration-500"
              style={{ width: `${progress}%` }}
            />
          </div>
        </div>

        {/* Processing Logs */}
        <div className="bg-black/20 backdrop-blur-lg rounded-xl p-6 border border-white/5 w-full">
          <div className="space-y-3">
            {logs.map((log, index) => (
              <div
                key={index}
                className="text-blue-300 font-mono text-sm opacity-0 animate-fadeIn"
                style={{ animationDelay: `${index * 0.2}s` }}
              >
                <span className="text-purple-400">&gt;</span> {log}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default FuturisticInterface;