export default function AnimatedBackground() {
  return (
    <div className="absolute inset-0 -z-10 overflow-hidden pointer-events-none">
      
      {/* Base Gradient */}
      <div className="absolute inset-0 z-[-1]  bg-linear-to-br from-blue-50 via-white to-cyan-100 dark:from-[#020617] dark:via-[#050811] dark:to-blue-950" />

      {/* SVG Fractal Filter */}
      <svg className="absolute w-0 h-0" aria-hidden="true">
        <defs>
          <filter id="fractalFlow" x="-100%" y="-100%" width="300%" height="300%">
            <feTurbulence 
              type="fractalNoise" 
              baseFrequency="0.012" 
              numOctaves="4" 
              result="noise"
            >
              <animate 
                attributeName="baseFrequency" 
                values="0.012;0.016;0.012" 
                dur="25s" 
                repeatCount="indefinite" 
              />
            </feTurbulence>
            <feDisplacementMap 
              in="SourceGraphic" 
              in2="noise" 
              scale="90" 
              xChannelSelector="R" 
              yChannelSelector="G" 
            />
          </filter>
        </defs>
      </svg>

      {/* Animated Fractal Layers */}
      <div className="absolute inset-0 z-0">
        {[...Array(10)].map((_, i) => {
          const size = 30 + i * 10;
          const delay = i * -5;
          const duration = (15 + i * 3) * 20;
          const x = i % 2 === 0 ? -15 + i * 12 : 10 + i * 10;
          const y = i % 3 === 0 ? -10 + i * 10 : 15 + i * 8;
          
          return (
            <div
              key={i}
              className="absolute rounded-full blur-2xl will-change-transform"
              style={{
                width: `${size}vw`,
                height: `${size}vw`,
                background: `radial-gradient(circle at center, ${
                  [
                    'rgba(59,130,246,0.8)',
                    'rgba(6,182,212,0.7)',
                    'rgba(99,102,241,0.8)',
                    'rgba(139,92,246,0.7)',
                    'rgba(236,72,153,0.6)',
                    'rgba(34,211,238,0.7)',
                  ][i]
                } 0%, transparent 70%)`,
                top: `${y}%`,
                left: `${x}%`,
                animation: `fractalFlow${i % 3} ${duration}s ease-in-out ${delay}s infinite`,
                filter: 'url(#fractalFlow)',
                opacity: 0.65,
              }}
            />
          );
        })}
      </div>

      {/* Keyframes */}
      <style>{`
        @keyframes fractalFlow0 {
          0%, 100% { transform: translate(0,0) rotate(0deg) scale(1); }
          25% { transform: translate(12vw, 18vh) rotate(120deg) scale(1.15); }
          50% { transform: translate(-8vw, 28vh) rotate(240deg) scale(0.85); }
          75% { transform: translate(18vw, -12vh) rotate(360deg) scale(1.05); }
        }
        @keyframes fractalFlow1 {
          0%, 100% { transform: translate(0,0) rotate(0deg) scale(1); }
          33% { transform: translate(-18vw, 22vh) rotate(-150deg) scale(1.2); }
          66% { transform: translate(14vw, -18vh) rotate(-300deg) scale(0.9); }
        }
        @keyframes fractalFlow2 {
          0%, 100% { transform: translate(0,0) rotate(0deg) scale(1); }
          50% { transform: translate(16vw, -25vh) rotate(180deg) scale(1.25); }
        }
      `}</style>
    </div>
  )
}