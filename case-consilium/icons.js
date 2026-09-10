// Render react-icons to PNG data-URIs for pptxgenjs
const React = require("react");
const ReactDOMServer = require("react-dom/server");
const sharp = require("sharp");
const Fa = require("react-icons/fa");
const Md = require("react-icons/md");

// name: [IconComponent]  (color applied at render time)
const DEFS = {
  target: Fa.FaBullseye, hotel: Fa.FaHotel, building: Fa.FaBuilding, hospital: Fa.FaHospitalAlt,
  home: Fa.FaHome, school: Fa.FaSchool, industry: Fa.FaIndustry, users: Fa.FaUsers,
  rupee: Fa.FaRupeeSign, chart: Fa.FaChartBar, chartline: Fa.FaChartLine, funnel: Fa.FaFilter,
  shield: Fa.FaShieldAlt, alert: Fa.FaExclamationTriangle, gear: Fa.FaCog, handshake: Fa.FaHandshake,
  pin: Fa.FaMapMarkerAlt, wrench: Fa.FaWrench, wifi: Fa.FaWifi, recycle: Fa.FaRecycle,
  flask: Fa.FaFlask, calendar: Fa.FaCalendarAlt, truck: Fa.FaTruck, certificate: Fa.FaCertificate,
  briefcase: Fa.FaBriefcase, drop: Fa.FaTint, leaf: Fa.FaLeaf, search: Fa.FaSearch,
  bolt: Fa.FaBolt, phone: Fa.FaPhoneAlt, doc: Fa.FaFileAlt, check: Fa.FaCheckCircle,
  clock: Fa.FaClock, eye: Fa.FaEye, lock: Fa.FaLock, route: Fa.FaRoute,
  bulb: Fa.FaLightbulb, flag: Fa.FaFlagCheckered, arrowr: Fa.FaArrowRight, star: Fa.FaStar,
  gavel: Fa.FaGavel, tag: Fa.FaTag, network: Fa.FaProjectDiagram, monitor: Md.MdMonitor,
  water: Md.MdWaterDrop, science: Md.MdScience, factory: Md.MdFactory, apartment: Md.MdApartment,
  trend: Md.MdTrendingUp, verified: Md.MdVerified, plumb: Md.MdPlumbing, sensors: Md.MdSensors,
};

async function buildIcons(colorMap) {
  // colorMap: { key: "#RRGGBB", ... } where key = `${name}_${variant}`
  const out = {};
  for (const [key, spec] of Object.entries(colorMap)) {
    const [name, hex] = spec;
    const Comp = DEFS[name];
    if (!Comp) throw new Error("unknown icon " + name);
    const svg = ReactDOMServer.renderToStaticMarkup(React.createElement(Comp, { color: hex, size: 256 }));
    const png = await sharp(Buffer.from(svg), { density: 300 }).resize(256, 256, { fit: "contain", background: { r: 0, g: 0, b: 0, alpha: 0 } }).png().toBuffer();
    out[key] = "image/png;base64," + png.toString("base64");
  }
  return out;
}

module.exports = { buildIcons };
