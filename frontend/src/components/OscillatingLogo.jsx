export default function OscillatingLogo() {
  const glowStyle = {
    animation: "oscillateAndGlow 10s ease-in-out infinite",
    boxShadow: `0 0 50px var(--glow-color)`,
    width: 192,
    height: 192,
    borderRadius: 96,
  };

  return <img src="/logo192.png" className="glow-dark-mode" style={glowStyle} />;
}
