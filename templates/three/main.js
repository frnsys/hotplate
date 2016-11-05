import './css/main.sass';
import * as THREE from 'three';
import Scene from './app/Scene';

var scene = new Scene();
var geometry = new THREE.BoxGeometry(1,1,1),
    material = new THREE.MeshLambertMaterial(),
    mesh = new THREE.Mesh(geometry, material);
mesh.position.set(0,0,0);
scene.scene.add(mesh);

function run() {
  requestAnimationFrame(run);
  scene.render();
}
run();
