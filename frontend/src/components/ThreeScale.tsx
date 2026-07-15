import { useRef } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';

interface ThreeScaleProps {
  outcome?: 'Conviction' | 'Acquittal' | null;
}

export default function ThreeScale({ outcome }: ThreeScaleProps) {
  const beamRef = useRef<THREE.Group>(null);
  const leftPanRef = useRef<THREE.Group>(null);
  const rightPanRef = useRef<THREE.Group>(null);

  // Target tilt angle based on outcome
  let targetAngle = 0;
  if (outcome === 'Conviction') {
    targetAngle = -0.25; // tilt left
  } else if (outcome === 'Acquittal') {
    targetAngle = 0.25; // tilt right
  }

  useFrame((state) => {
    if (beamRef.current && leftPanRef.current && rightPanRef.current) {
      // Smoothly interpolate beam rotation
      beamRef.current.rotation.z = THREE.MathUtils.lerp(
        beamRef.current.rotation.z,
        targetAngle,
        0.05
      );

      // Keep pans vertical by counter-rotating them
      leftPanRef.current.rotation.z = -beamRef.current.rotation.z;
      rightPanRef.current.rotation.z = -beamRef.current.rotation.z;

      // Gentle floating animation
      const t = state.clock.getElapsedTime();
      beamRef.current.position.y = Math.sin(t * 1.5) * 0.05 + 0.5;
    }
  });

  return (
    <group position={[0, -0.5, 0]}>
      {/* Base */}
      <mesh castShadow receiveShadow position={[0, -1.1, 0]}>
        <cylinderGeometry args={[1, 1.1, 0.2, 32]} />
        <meshPhysicalMaterial
          color="#121214"
          roughness={0.4}
          metalness={0.9}
          clearcoat={1}
          clearcoatRoughness={0.1}
        />
      </mesh>

      {/* Main Stand Vertical Pole */}
      <mesh castShadow receiveShadow position={[0, 0, 0]}>
        <cylinderGeometry args={[0.08, 0.1, 2.0, 16]} />
        <meshStandardMaterial
          color="#fbbf24" // gold-brass
          roughness={0.2}
          metalness={0.9}
        />
      </mesh>

      {/* Center cap / accent on pole */}
      <mesh castShadow position={[0, 0.9, 0]}>
        <sphereGeometry args={[0.18, 16, 16]} />
        <meshStandardMaterial
          color="#d97706"
          roughness={0.25}
          metalness={0.9}
        />
      </mesh>

      {/* Tilting Beam & Pans group */}
      <group ref={beamRef} position={[0, 0.8, 0]}>
        {/* Horizontal Beam */}
        <mesh castShadow receiveShadow rotation={[0, 0, 0]}>
          <cylinderGeometry args={[0.04, 0.04, 2.2, 16]} />
          {/* Rotate cylinder to lie horizontally along X axis */}
          <primitive object={new THREE.Quaternion().setFromAxisAngle(new THREE.Vector3(0, 0, 1), Math.PI / 2)} attach="quaternion" />
          <meshStandardMaterial
            color="#fbbf24"
            roughness={0.2}
            metalness={0.9}
          />
        </mesh>

        {/* Center pivot joint */}
        <mesh position={[0, 0, 0.08]}>
          <sphereGeometry args={[0.1, 16, 16]} />
          <meshStandardMaterial
            color="#f59e0b"
            roughness={0.1}
            metalness={0.95}
          />
        </mesh>

        {/* Left Side Hanger & Pan */}
        <group ref={leftPanRef} position={[-1.1, -0.1, 0]}>
          {/* Left string/chain 1 */}
          <mesh position={[-0.15, -0.4, 0]} rotation={[0, 0, 0.3]}>
            <cylinderGeometry args={[0.005, 0.005, 0.9, 8]} />
            <meshStandardMaterial color="#fbbf24" roughness={0.5} />
          </mesh>
          {/* Left string/chain 2 */}
          <mesh position={[0.15, -0.4, 0]} rotation={[0, 0, -0.3]}>
            <cylinderGeometry args={[0.005, 0.005, 0.9, 8]} />
            <meshStandardMaterial color="#fbbf24" roughness={0.5} />
          </mesh>
          {/* Left Pan */}
          <mesh castShadow receiveShadow position={[0, -0.85, 0]}>
            <cylinderGeometry args={[0.45, 0.45, 0.03, 32]} />
            <meshPhysicalMaterial
              color="#fbbf24"
              roughness={0.1}
              metalness={0.8}
              transmission={0.4} // semi-glass look for the pan
              thickness={0.2}
            />
          </mesh>
        </group>

        {/* Right Side Hanger & Pan */}
        <group ref={rightPanRef} position={[1.1, -0.1, 0]}>
          {/* Right string/chain 1 */}
          <mesh position={[-0.15, -0.4, 0]} rotation={[0, 0, 0.3]}>
            <cylinderGeometry args={[0.005, 0.005, 0.9, 8]} />
            <meshStandardMaterial color="#fbbf24" roughness={0.5} />
          </mesh>
          {/* Right string/chain 2 */}
          <mesh position={[0.15, -0.4, 0]} rotation={[0, 0, -0.3]}>
            <cylinderGeometry args={[0.005, 0.005, 0.9, 8]} />
            <meshStandardMaterial color="#fbbf24" roughness={0.5} />
          </mesh>
          {/* Right Pan */}
          <mesh castShadow receiveShadow position={[0, -0.85, 0]}>
            <cylinderGeometry args={[0.45, 0.45, 0.03, 32]} />
            <meshPhysicalMaterial
              color="#fbbf24"
              roughness={0.1}
              metalness={0.8}
              transmission={0.4}
              thickness={0.2}
            />
          </mesh>
        </group>
      </group>
    </group>
  );
}
