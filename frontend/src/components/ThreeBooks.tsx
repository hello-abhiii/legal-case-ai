import { useRef, useState } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';

export default function ThreeBooks() {
  const topBookRef = useRef<THREE.Group>(null);
  const [hovered, setHovered] = useState(false);

  useFrame(() => {
    if (!topBookRef.current) return;
    
    // Smoothly slide the top book forward/rotate it slightly when hovered
    const targetX = hovered ? -0.2 : 0;
    const targetZ = hovered ? 0.15 : 0.05; // slightly askew
    
    topBookRef.current.position.x = THREE.MathUtils.lerp(topBookRef.current.position.x, targetX, 0.1);
    topBookRef.current.rotation.y = THREE.MathUtils.lerp(topBookRef.current.rotation.y, targetZ, 0.1);

    // Floating stack effect
    const t = performance.now() / 1000;
    const group = topBookRef.current.parent;
    if (group) {
      group.position.y = Math.sin(t * 1.2) * 0.03 - 0.2;
    }
  });

  return (
    <group 
      position={[0, -0.2, 0]}
      onPointerOver={() => setHovered(true)}
      onPointerOut={() => setHovered(false)}
    >
      {/* Bottom Book (Large - Burgundy) */}
      <group position={[0, -0.6, 0]} rotation={[0, -0.1, 0]}>
        {/* Pages (white inner box) */}
        <mesh castShadow receiveShadow position={[0.05, 0, 0]}>
          <boxGeometry args={[1.3, 0.18, 1.0]} />
          <meshStandardMaterial color="#fafaf9" roughness={0.7} />
        </mesh>
        {/* Leather Cover (colored thin borders enclosing the pages) */}
        <mesh castShadow position={[-0.05, 0, 0]}>
          <boxGeometry args={[1.35, 0.22, 1.05]} />
          <meshPhysicalMaterial
            color="#450a0a" // Dark wine/red
            roughness={0.6}
            metalness={0.1}
            clearcoat={0.3}
          />
        </mesh>
        {/* Gold Spine Lines */}
        <mesh position={[-0.73, 0, 0]}>
          <boxGeometry args={[0.01, 0.23, 0.95]} />
          <meshStandardMaterial color="#fbbf24" metalness={0.9} roughness={0.1} />
        </mesh>
      </group>

      {/* Middle Book (Medium - Navy Blue) */}
      <group position={[0, -0.38, 0]} rotation={[0, 0.15, 0]}>
        {/* Pages */}
        <mesh castShadow receiveShadow position={[0.05, 0, 0]}>
          <boxGeometry args={[1.2, 0.18, 0.9]} />
          <meshStandardMaterial color="#f5f5f4" roughness={0.7} />
        </mesh>
        {/* Cover */}
        <mesh castShadow position={[-0.03, 0, 0]}>
          <boxGeometry args={[1.25, 0.22, 0.95]} />
          <meshPhysicalMaterial
            color="#0f172a" // Slate/Navy
            roughness={0.5}
            metalness={0.1}
            clearcoat={0.3}
          />
        </mesh>
        {/* Spine line */}
        <mesh position={[-0.66, 0, 0]}>
          <boxGeometry args={[0.01, 0.23, 0.85]} />
          <meshStandardMaterial color="#fbbf24" metalness={0.9} roughness={0.1} />
        </mesh>
      </group>

      {/* Top Book (Small - Forest Green, slides on hover) */}
      <group ref={topBookRef} position={[0, -0.16, 0]} rotation={[0, 0.05, 0]}>
        {/* Pages */}
        <mesh castShadow receiveShadow position={[0.04, 0, 0]}>
          <boxGeometry args={[1.1, 0.18, 0.8]} />
          <meshStandardMaterial color="#fafaf9" roughness={0.7} />
        </mesh>
        {/* Cover */}
        <mesh castShadow position={[-0.02, 0, 0]}>
          <boxGeometry args={[1.15, 0.22, 0.85]} />
          <meshPhysicalMaterial
            color="#064e3b" // Forest Green
            roughness={0.5}
            metalness={0.1}
            clearcoat={0.3}
          />
        </mesh>
        {/* Spine line */}
        <mesh position={[-0.6, 0, 0]}>
          <boxGeometry args={[0.01, 0.23, 0.75]} />
          <meshStandardMaterial color="#fbbf24" metalness={0.9} roughness={0.1} />
        </mesh>
      </group>
    </group>
  );
}
