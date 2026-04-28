import { useState } from "react";
import { MobileApp } from "./components/MobileApp";
import { WorkshopDashboard } from "./components/WorkshopDashboard";
import SmartphoneIcon from "@mui/icons-material/Smartphone";
import ComputerIcon from "@mui/icons-material/Computer";
import CheckCircleIcon from "@mui/icons-material/CheckCircle";

type ViewMode = "mobile" | "workshop";

export default function App() {
  const [viewMode, setViewMode] = useState<ViewMode>("mobile");

  return (
    <div className="size-full flex flex-col items-center justify-center bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 p-8">
      {/* Header */}
      <div className="mb-6 text-center">
        <h1 className="text-3xl font-bold text-white mb-2">
          Plataforma Inteligente de Atención de Emergencias
          Vehiculares
        </h1>
        <p className="text-blue-200">
          Sistema de Asistencia con IA Multimodal
        </p>
      </div>

      {/* View Toggle */}
      <div className="mb-6 bg-white/10 backdrop-blur-sm rounded-2xl p-2 flex gap-2">
        <button
          onClick={() => setViewMode("mobile")}
          className={`flex items-center gap-2 px-6 py-3 rounded-xl font-bold transition-all ${
            viewMode === "mobile"
              ? "bg-white text-blue-900 shadow-lg"
              : "text-white hover:bg-white/10"
          }`}
        >
          <SmartphoneIcon sx={{ fontSize: 24 }} />
          App Cliente (Móvil)
        </button>
        <button
          onClick={() => setViewMode("workshop")}
          className={`flex items-center gap-2 px-6 py-3 rounded-xl font-bold transition-all ${
            viewMode === "workshop"
              ? "bg-white text-blue-900 shadow-lg"
              : "text-white hover:bg-white/10"
          }`}
        >
          <ComputerIcon sx={{ fontSize: 24 }} />
          Panel Taller (Web)
        </button>
      </div>

      {/* Main Content */}
      <div className="w-full max-w-7xl flex justify-center">
        {viewMode === "mobile" ? (
          <MobileApp />
        ) : (
          <WorkshopDashboard />
        )}
      </div>

      {/* Footer Info */}
      <div className="mt-6 text-center text-sm text-blue-200">
        <p className="flex items-center justify-center gap-2">
          <CheckCircleIcon sx={{ fontSize: 18 }} />
          Prototipo interactivo con navegación completa
        </p>
        <p className="text-xs mt-1 text-blue-300">
          Mobile: Reportes multimodales (GPS + Foto + Voz +
          Texto) | Web: Gestión completa de talleres y técnicos
        </p>
      </div>
    </div>
  );
}