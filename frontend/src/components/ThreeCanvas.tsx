import React, { useRef, Suspense } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';
import * as THREE from 'three';
import ThreeScale from './ThreeScale';
import ThreeGavel from './ThreeGavel';
import ThreeBooks from './ThreeBooks';

interface ThreeCanvasProps {
  activeObject: 'scale' | 'gavel' | 'books';
  outcome?: 'Conviction' | 'Acquittal' | null;
}

// Subcomponent to handle cursor-tracking parallax
function InteractiveContainer({ children }: { children: React.ReactNode }) {
  const containerRef = useRef<THREE.Group>(null);

  useFrame(({ pointer }) => {
    if (containerRef.current) {
      // Smoothly tilt container based on mouse pointer
      containerRef.current.rotation.y = THREE.MathUtils.lerp(
        containerRef.current.rotation.y,
        pointer.x * 0.3,
        0.05
      );
      containerRef.current.rotation.x = THREE.MathUtils.lerp(
        containerRef.current.rotation.x,
        -pointer.y * 0.2,
        0.05
      );
    }
  });

  return <group ref={containerRef}>{children}</group>;
}

export default function ThreeCanvas({ activeObject, outcome }: ThreeCanvasProps) {
  return (
    <div style={{ width: '100%', height: '100%', minHeight: '350px', position: 'relative' }}>
      <Canvas
        shadows
        camera={{ position: [0, 0.2, 3.5], fov: 45 }}
        gl={{ antialias: true, alpha: true }}
      >
        {/* Lights */}
        <ambientLight intensity={0.6} />
        
        {/* Directional light for crisp shadows */}
        <directionalLight
          castShadow
          position={[5, 8, 5]}
          intensity={1.2}
          shadow-mapSize-width={1024}
          shadow-mapSize-height={1024}
          shadow-camera-near={0.5}
          shadow-camera-far={20}
        />

        {/* Spot light for dramatic highlight */}
        <spotLight
          position={[0, 5, 2]}
          intensity={0.8}
          angle={Math.PI / 4}
          penumbra={1}
          castShadow
        />

        {/* Soft blue point light on left side */}
        <pointLight position={[-4, 0, 1]} intensity={0.6} color="#3b82f6" />
        
        {/* Soft purple point light on right side */}
        <pointLight position={[4, 0, 1]} intensity={0.6} color="#8b5cf6" />

        <Suspense fallback={null}>
          <InteractiveContainer>
            {activeObject === 'scale' && <ThreeScale outcome={outcome} />}
            {activeObject === 'gavel' && <ThreeGavel />}
            {activeObject === 'books' && <ThreeBooks />}
          </InteractiveContainer>
        </Suspense>

        {/* Standard subtle OrbitControls */}
        <OrbitControls
          enableZoom={false}
          enablePan={false}
          minPolarAngle={Math.PI / 2.5}
          maxPolarAngle={Math.PI / 1.8}
        />
      </Canvas>
    </div>
  );
}
