import React, { useEffect, useRef } from "react";
import { Stage, Layer, Rect, Text, Group } from "react-konva";
import Konva from "konva";
import { useSceneStore } from "../state/useSceneStore";

export default function CanvasPlayer() {
  const { width, height } = useSceneStore((s) => s.canvasDims);
  const runtimeScene = useSceneStore((s) => s.runtimeScene);
  const currentFrame = useSceneStore((s) => s.currentFrame);

  const frame = runtimeScene[currentFrame] || null;

  // highlight rect ref
  const highlightRef = useRef(null);

  // animate highlight when frame changes
  useEffect(() => {
    if (highlightRef.current) {
      new Konva.Tween({
        node: highlightRef.current,
        duration: 0.3,
        opacity: 0.3,
        fill: "#4f46e5",
        easing: Konva.Easings.EaseInOut,
      }).play();
    }
  }, [currentFrame]);


  // Compute variable block positions (grid)
  const getVariablePositions = (vars) => {
    const entries = Object.entries(vars);
    const startX = 40;
    const startY = 120;
    const gap = 160;

    return entries.map(([key, val], index) => ({
      key,
      val,
      x: startX + index * gap,
      y: startY,
    }));
  };

  const prevFrameRef = useRef(null);
  useEffect(() => {
    prevFrameRef.current = frame;
  }, [frame]);

  const detectVariableChanges = (prev, curr) => {
    const changes = {};

    const prevVars = prev ? prev.locals : {};
    const currVars = curr.locals;

    for (const key in currVars) {
      if (!(key in prevVars)) {
        changes[key] = "created";
      } else if (prevVars[key] !== currVars[key]) {
        changes[key] = "updated";
      } else {
        changes[key] = "same";
      }
    }

    return changes;
  };

const varChanges = detectVariableChanges(prevFrameRef.current, frame);




  return (
    <div
      style={{
        width: width + "px",
        height: height + "px",
        border: "1px solid #333",
        background: "black",
      }}
    >
      <Stage width={width} height={height}>
        <Layer>
          {/* Background */}
          <Rect x={0} y={0} width={width} height={height} fill="#0f0f0f" />

          {/* If no frame */}
          {!frame && (
            <Text
              text="Run code to generate animation"
              fontSize={28}
              fill="white"
              x={width / 2 - 180}
              y={height / 2 - 20}
            />
          )}

          {frame && (
            <Group>
              {/* Highlight */}
              <Rect
                ref={highlightRef}
                x={20}
                y={20}
                width={width - 40}
                height={60}
                opacity={0}
                cornerRadius={8}
              />

              {/* Code line */}
              <Text
                text={`Line ${frame.lineno}: ${frame.code}`}
                x={40}
                y={40}
                fontSize={28}
                fill="white"
              />

              {/* Variables */}
              
              {frame &&
                getVariablePositions(frame.locals).map((item) => (
                  <Group key={item.key}>
                    {/* Animated variable box */}
                    <Rect
                      ref={(node) => {
                        if (!node) return;
                        
                        // apply entrance animation for new variables
                        if (varChanges[item.key] === "created") {
                          node.y(item.y - 40);
                          node.opacity(0);
                          new Konva.Tween({
                            node,
                            duration: 0.4,
                            y: item.y,
                            opacity: 1,
                            easing: Konva.Easings.EaseOut,
                          }).play();
                        }
                    
                        // apply highlight pulse for updated variables
                        if (varChanges[item.key] === "updated") {
                          new Konva.Tween({
                            node,
                            duration: 0.3,
                            fill: "#3730a3",
                            easing: Konva.Easings.EaseInOut,
                            onFinish: () => {
                              new Konva.Tween({
                                node,
                                duration: 0.3,
                                fill: "#1e1e2f",
                              }).play();
                            },
                          }).play();
                        }
                      }}
                      x={item.x}
                      y={item.y}
                      width={120}
                      height={70}
                      cornerRadius={10}
                      fill="#1e1e2f"
                      stroke={varChanges[item.key] === "updated" ? "#4ade80" : "#6366f1"}
                      strokeWidth={varChanges[item.key] === "updated" ? 3 : 2}
                    />
                
                    {/* variable name */}
                    <Text
                      text={item.key}
                      x={item.x + 10}
                      y={item.y + 10}
                      fontSize={20}
                      fill="#a5b4fc"
                    />
                
                    {/* variable value with animation */}
                    <Text
                      ref={(node) => {
                        if (!node) return;
                        
                        // new variable value animation
                        if (varChanges[item.key] === "created") {
                          node.opacity(0);
                          new Konva.Tween({
                            node,
                            duration: 0.4,
                            opacity: 1,
                            easing: Konva.Easings.EaseOut,
                          }).play();
                        }
                    
                        // updated value animation (color + pulse)
                        if (varChanges[item.key] === "updated") {
                          new Konva.Tween({
                            node,
                            duration: 0.3,
                            scaleX: 1.2,
                            scaleY: 1.2,
                            fill: "#4ade80",
                            onFinish: () => {
                              new Konva.Tween({
                                node,
                                duration: 0.3,
                                scaleX: 1,
                                scaleY: 1,
                                fill: "#4ade80",
                              }).play();
                            },
                          }).play();
                        }
                      }}
                      text={String(item.val)}
                      x={item.x + 10}
                      y={item.y + 40}
                      fontSize={22}
                      fill="#4ade80"
                    />
                  </Group>
                ))}



              {/* Output */}
              {frame.output && (
                <Text
                  text={`Output: ${frame.output}`}
                  x={40}
                  y={180}
                  fontSize={24}
                  fill="#60a5fa"
                />
              )}
            </Group>
          )}
        </Layer>
      </Stage>
    </div>
  );
}
