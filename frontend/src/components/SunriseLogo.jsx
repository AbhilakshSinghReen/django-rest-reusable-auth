export default function SunriseLogo() {
  const glowStyle = {
    animation: "sunRise 10s ease-in-out",
    boxShadow: `0 0 100px var(--glow-color)`,
    width: 192,
    height: 192,
    borderRadius: 96,
  };

  return <img src="/logo192.png" className="glow-light-mode" style={glowStyle} />;
}
