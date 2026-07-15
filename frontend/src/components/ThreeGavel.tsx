import { useRef, useState } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';

export default function ThreeGavel() {
  const gavelRef = useRef<THREE.Group>(null);
  const [isStriking, setIsStriking] = useState(false);
  const strikeStartTime = useRef<number>(0);

  const handleClick = () => {
    if (!isStriking) {
      setIsStriking(true);
      strikeStartTime.current = performance.now();
    }
  };

  useFrame(() => {
    if (!gavelRef.current) return;

    if (isStriking) {
      const elapsed = (performance.now() - strikeStartTime.current) / 1000;
      const duration = 0.5; // Strike animation takes 0.5 seconds

      if (elapsed >= duration) {
        setIsStriking(false);
        gavelRef.current.rotation.x = -0.4; // Reset to default tilt
      } else {
        // Build a strike swing using a sine curve for springy bounce
        // Starts at default, swings down to hit sound block (rotation.x = 0.5), then rebounds back.
        const progress = elapsed / duration;
        const swing = Math.sin(progress * Math.PI);
        gavelRef.current.rotation.x = -0.4 + swing * 0.9;
      }
    } else {
      // Gentle floating animation when resting
      const t = performance.now() / 1000;
      gavelRef.current.position.y = Math.sin(t * 1.8) * 0.04 - 0.1;
    }
  });

  return (
    <group position={[0, -0.4, 0]} onClick={handleClick}>
      {/* Sound Block at the bottom */}
      <mesh castShadow receiveShadow position={[0, -0.8, 0]}>
        <cylinderGeometry args={[0.9, 1.0, 0.25, 32]} />
        <meshPhysicalMaterial
          color="#18181b"
          roughness={0.5}
          metalness={0.2}
          clearcoat={0.8}
          clearcoatRoughness={0.2}
        />
      </mesh>
      
      {/* Sound Block golden accent ring */}
      <mesh position={[0, -0.68, 0]}>
        <cylinderGeometry args={[0.85, 0.85, 0.02, 32]} />
        <meshStandardMaterial
          color="#fbbf24"
          roughness={0.2}
          metalness={0.9}
        />
      </mesh>

      {/* Gavel Group (Head + Handle) */}
      <group ref={gavelRef} position={[0, -0.1, -0.2]} rotation={[-0.4, 0, 0.2]}>
        {/* Handle */}
        <mesh castShadow position={[0, 0, 0.6]} rotation={[Math.PI / 2, 0, 0]}>
          <cylinderGeometry args={[0.04, 0.05, 1.2, 16]} />
          <meshPhysicalMaterial
            color="#27272a"
            roughness={0.3}
            metalness={0.8}
            clearcoat={0.5}
          />
        </mesh>

        {/* Handle Gold Accent Tip */}
        <mesh position={[0, 0, 1.22]} rotation={[Math.PI / 2, 0, 0]}>
          <cylinderGeometry args={[0.04, 0.04, 0.05, 16]} />
          <meshStandardMaterial
            color="#fbbf24"
            roughness={0.1}
            metalness={0.9}
          />
        </mesh>

        {/* Gavel Head */}
        <mesh castShadow position={[0, 0, 0]} rotation={[0, 0, Math.PI / 2]}>
          <cylinderGeometry args={[0.18, 0.18, 0.45, 24]} />
          <meshPhysicalMaterial
            color="#1e1b4b" // Deep dark purple wood
            roughness={0.4}
            metalness={0.1}
            clearcoat={0.8}
          />
        </mesh>

        {/* Gavel Head Left Gold Ring */}
        <mesh position={[-0.15, 0, 0]} rotation={[0, 0, Math.PI / 2]}>
          <cylinderGeometry args={[0.182, 0.182, 0.03, 24]} />
          <meshStandardMaterial
            color="#fbbf24"
            roughness={0.15}
            metalness={0.9}
          />
        </mesh>

        {/* Gavel Head Right Gold Ring */}
        <mesh position={[0.15, 0, 0]} rotation={[0, 0, Math.PI / 2]}>
          <cylinderGeometry args={[0.182, 0.182, 0.03, 24]} />
          <meshStandardMaterial
            color="#fbbf24"
            roughness={0.15}
            metalness={0.9}
          />
        </mesh>
      </group>
    </group>
  );
}
