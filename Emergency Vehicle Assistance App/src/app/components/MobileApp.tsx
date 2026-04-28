import { useState } from 'react';
import HomeIcon from '@mui/icons-material/Home';
import HistoryIcon from '@mui/icons-material/History';
import PersonIcon from '@mui/icons-material/Person';
import LocationOnIcon from '@mui/icons-material/LocationOn';
import CameraAltIcon from '@mui/icons-material/CameraAlt';
import MicIcon from '@mui/icons-material/Mic';
import DescriptionIcon from '@mui/icons-material/Description';
import WarningIcon from '@mui/icons-material/Warning';
import PhoneIcon from '@mui/icons-material/Phone';
import WhatsAppIcon from '@mui/icons-material/WhatsApp';
import CreditCardIcon from '@mui/icons-material/CreditCard';
import DirectionsCarIcon from '@mui/icons-material/DirectionsCar';
import ChevronRightIcon from '@mui/icons-material/ChevronRight';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import AccessTimeIcon from '@mui/icons-material/AccessTime';
import HourglassEmptyIcon from '@mui/icons-material/HourglassEmpty';
import WifiIcon from '@mui/icons-material/Wifi';
import SignalCellularAltIcon from '@mui/icons-material/SignalCellularAlt';
import BatteryFullIcon from '@mui/icons-material/BatteryFull';
import FlashOnIcon from '@mui/icons-material/FlashOn';
import BarChartIcon from '@mui/icons-material/BarChart';
import ImageIcon from '@mui/icons-material/Image';
import RadioIcon from '@mui/icons-material/Radio';
import BuildIcon from '@mui/icons-material/Build';
import PendingActionsIcon from '@mui/icons-material/PendingActions';
import PaymentIcon from '@mui/icons-material/Payment';

type Screen = 'home' | 'vehicles' | 'add-vehicle' | 'report' | 'ai-diagnosis' | 'tracking' | 'profile' | 'payment' | 'history' | 'my-services';

export function MobileApp() {
  const [currentScreen, setCurrentScreen] = useState<Screen>('home');
  const [isRecording, setIsRecording] = useState(false);
  const [aiProgress, setAiProgress] = useState(0);

  const handleReportEmergency = () => {
    setCurrentScreen('ai-diagnosis');
    let progress = 0;
    const interval = setInterval(() => {
      progress += 10;
      setAiProgress(progress);
      if (progress >= 100) {
        clearInterval(interval);
        setTimeout(() => setCurrentScreen('tracking'), 500);
      }
    }, 200);
  };

  return (
    <div className="w-full max-w-[400px] h-[800px] bg-white rounded-3xl shadow-2xl overflow-hidden flex flex-col">
      {/* Status Bar */}
      <div className="bg-red-600 text-white px-4 py-2 flex justify-between items-center text-xs">
        <span>6:55</span>
        <div className="flex gap-2 items-center">
          <SignalCellularAltIcon sx={{ fontSize: 14 }} />
          <WifiIcon sx={{ fontSize: 14 }} />
          <div className="flex items-center gap-1">
            <BatteryFullIcon sx={{ fontSize: 14 }} />
            <span>100%</span>
          </div>
        </div>
      </div>

      {/* Header */}
      <div className="bg-red-600 text-white px-4 py-4">
        {currentScreen !== 'home' && (
          <button onClick={() => setCurrentScreen('home')} className="mb-2">
            <ArrowBackIcon sx={{ fontSize: 28 }} />
          </button>
        )}
        <h1 className="text-xl font-bold">Asistencia Vehicular</h1>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-y-auto bg-gray-50">
        {currentScreen === 'home' && <HomeScreen setScreen={setCurrentScreen} />}
        {currentScreen === 'vehicles' && <VehiclesScreen setScreen={setCurrentScreen} />}
        {currentScreen === 'add-vehicle' && <AddVehicleScreen setScreen={setCurrentScreen} />}
        {currentScreen === 'report' && <ReportScreen onSubmit={handleReportEmergency} isRecording={isRecording} setIsRecording={setIsRecording} />}
        {currentScreen === 'ai-diagnosis' && <AIDiagnosisScreen progress={aiProgress} />}
        {currentScreen === 'tracking' && <TrackingScreen setScreen={setCurrentScreen} />}
        {currentScreen === 'my-services' && <MyServicesScreen setScreen={setCurrentScreen} />}
        {currentScreen === 'profile' && <ProfileScreen />}
        {currentScreen === 'payment' && <PaymentScreen />}
        {currentScreen === 'history' && <HistoryScreen />}
      </div>

      {/* Bottom Navigation */}
      <div className="bg-white border-t border-gray-200 px-2 py-3 flex justify-around items-center">
        <button onClick={() => setCurrentScreen('home')} className={`flex flex-col items-center gap-1 ${currentScreen === 'home' ? 'text-red-600' : 'text-gray-500'}`}>
          <HomeIcon sx={{ fontSize: 24 }} />
          <span className="text-xs">Inicio</span>
        </button>
        <button onClick={() => setCurrentScreen('my-services')} className={`flex flex-col items-center gap-1 ${currentScreen === 'my-services' ? 'text-red-600' : 'text-gray-500'}`}>
          <BuildIcon sx={{ fontSize: 24 }} />
          <span className="text-xs">Atenciones</span>
        </button>
        <button onClick={() => setCurrentScreen('history')} className={`flex flex-col items-center gap-1 ${currentScreen === 'history' ? 'text-red-600' : 'text-gray-500'}`}>
          <HistoryIcon sx={{ fontSize: 24 }} />
          <span className="text-xs">Historial</span>
        </button>
        <button onClick={() => setCurrentScreen('profile')} className={`flex flex-col items-center gap-1 ${currentScreen === 'profile' ? 'text-red-600' : 'text-gray-500'}`}>
          <PersonIcon sx={{ fontSize: 24 }} />
          <span className="text-xs">Perfil</span>
        </button>
      </div>
    </div>
  );
}

function HomeScreen({ setScreen }: { setScreen: (screen: Screen) => void }) {
  return (
    <div className="p-4 space-y-4">
      {/* Status Card */}
      <div className="bg-green-600 text-white rounded-2xl p-4 flex items-center gap-3">
        <CheckCircleIcon sx={{ fontSize: 36 }} />
        <div>
          <p className="font-bold">Estado: Activo</p>
          <p className="text-sm opacity-90">Listo para reportar incidentes</p>
        </div>
      </div>

      {/* Active Services Alert */}
      <div className="bg-blue-50 border-2 border-blue-400 rounded-xl p-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <PendingActionsIcon sx={{ fontSize: 24, color: '#2563eb' }} />
            <div>
              <p className="text-sm font-bold text-blue-800">Tienes 1 servicio en proceso</p>
              <p className="text-xs text-blue-600">+ 1 pago pendiente</p>
            </div>
          </div>
          <button onClick={() => setScreen('my-services')} className="bg-blue-600 text-white px-3 py-1 rounded-lg text-xs font-bold">
            Ver
          </button>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="space-y-3">
        <h2 className="font-bold text-gray-800">Acciones Rápidas</h2>

        <button onClick={() => setScreen('report')} className="w-full bg-orange-500 hover:bg-orange-600 text-white rounded-2xl p-4 flex items-center justify-between transition-colors">
          <div className="flex items-center gap-3">
            <WarningIcon sx={{ fontSize: 32 }} />
            <div className="text-left">
              <p className="font-bold">Reportar Incidente</p>
              <p className="text-sm opacity-90">Describe tu emergencia</p>
            </div>
          </div>
          <ChevronRightIcon sx={{ fontSize: 28 }} />
        </button>

        <button onClick={() => setScreen('my-services')} className="w-full bg-blue-500 hover:bg-blue-600 text-white rounded-2xl p-4 flex items-center justify-between transition-colors">
          <div className="flex items-center gap-3">
            <BuildIcon sx={{ fontSize: 32 }} />
            <div className="text-left">
              <p className="font-bold">Mis Atenciones</p>
              <p className="text-sm opacity-90">Servicios activos y pendientes</p>
            </div>
          </div>
          <ChevronRightIcon sx={{ fontSize: 28 }} />
        </button>

        <button onClick={() => setScreen('vehicles')} className="w-full bg-yellow-500 hover:bg-yellow-600 text-white rounded-2xl p-4 flex items-center justify-between transition-colors">
          <div className="flex items-center gap-3">
            <DirectionsCarIcon sx={{ fontSize: 32 }} />
            <div className="text-left">
              <p className="font-bold">Mis Vehículos</p>
              <p className="text-sm opacity-90">Gestiona tus vehículos</p>
            </div>
          </div>
          <ChevronRightIcon sx={{ fontSize: 28 }} />
        </button>
      </div>
    </div>
  );
}

function VehiclesScreen({ setScreen }: { setScreen: (screen: Screen) => void }) {
  const vehicles = [
    { id: 1, plate: 'ABC-123', model: 'Toyota Corolla 2020', brand: 'Toyota' },
    { id: 2, plate: 'XYZ-789', model: 'Honda Civic 2019', brand: 'Honda' }
  ];

  return (
    <div className="p-4 space-y-4">
      <h2 className="font-bold text-gray-800">Mis Vehículos</h2>

      <div className="space-y-3">
        {vehicles.map(vehicle => (
          <div key={vehicle.id} className="bg-white rounded-xl p-4 shadow-sm border border-gray-200">
            <div className="flex items-center gap-3">
              <div className="bg-blue-100 p-3 rounded-lg">
                <DirectionsCarIcon sx={{ fontSize: 28, color: '#2563eb' }} />
              </div>
              <div className="flex-1">
                <p className="font-bold text-gray-800">{vehicle.plate}</p>
                <p className="text-sm text-gray-600">{vehicle.model}</p>
              </div>
            </div>
          </div>
        ))}
      </div>

      <button onClick={() => setScreen('add-vehicle')} className="w-full bg-blue-600 text-white rounded-xl p-4 font-bold">
        + Agregar Vehículo
      </button>
    </div>
  );
}

function AddVehicleScreen({ setScreen }: { setScreen: (screen: Screen) => void }) {
  return (
    <div className="p-4 space-y-4">
      <h2 className="font-bold text-gray-800">Registrar Vehículo</h2>

      <div className="space-y-3">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Placa</label>
          <input type="text" placeholder="ABC-123" className="w-full border border-gray-300 rounded-lg p-3" />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Marca</label>
          <input type="text" placeholder="Toyota" className="w-full border border-gray-300 rounded-lg p-3" />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Modelo</label>
          <input type="text" placeholder="Corolla 2020" className="w-full border border-gray-300 rounded-lg p-3" />
        </div>

        <button onClick={() => setScreen('vehicles')} className="w-full bg-blue-600 text-white rounded-xl p-4 font-bold mt-4">
          Guardar Vehículo
        </button>
      </div>
    </div>
  );
}

function ReportScreen({ onSubmit, isRecording, setIsRecording }: { onSubmit: () => void; isRecording: boolean; setIsRecording: (val: boolean) => void }) {
  const [photoTaken, setPhotoTaken] = useState(false);
  const [hasAudio, setHasAudio] = useState(false);

  const handleTakePhoto = () => {
    setPhotoTaken(true);
    setTimeout(() => setPhotoTaken(false), 2000);
  };

  const handleRecordAudio = () => {
    setIsRecording(true);
    setTimeout(() => {
      setIsRecording(false);
      setHasAudio(true);
    }, 3000);
  };

  return (
    <div className="p-4 space-y-4">
      <h2 className="font-bold text-gray-800">Reporte Rápido</h2>
      <p className="text-sm text-gray-600">Tu ubicación se detectó automáticamente</p>

      {/* GPS Auto-detected */}
      <div className="bg-blue-50 border-2 border-blue-300 rounded-xl p-3 flex items-center gap-3">
        <LocationOnIcon sx={{ fontSize: 28, color: '#2563eb' }} />
        <div className="flex-1">
          <p className="text-sm font-bold text-gray-800">Ubicación Detectada</p>
          <p className="text-xs text-gray-600">Av. Arequipa 1234, Lima, Perú</p>
        </div>
        <CheckCircleIcon sx={{ fontSize: 24, color: '#16a34a' }} />
      </div>

      {/* Quick Report Container */}
      <div className="bg-white rounded-2xl p-4 shadow-lg border-2 border-orange-500 space-y-3">
        <h3 className="font-bold text-orange-600 flex items-center gap-2">
          <WarningIcon sx={{ fontSize: 20 }} />
          Captura Evidencia
        </h3>

        {/* Photo Quick Action */}
        <button
          onClick={handleTakePhoto}
          className={`w-full ${photoTaken ? 'bg-green-600' : 'bg-green-500'} hover:bg-green-600 text-white rounded-xl p-4 transition-all`}
        >
          <div className="flex items-center justify-center gap-3">
            <CameraAltIcon sx={{ fontSize: 32 }} />
            <div className="text-left flex-1">
              <p className="font-bold">{photoTaken ? '✓ Foto Capturada' : 'Tomar Foto del Vehículo'}</p>
              <p className="text-sm opacity-90">Captura el daño o problema</p>
            </div>
          </div>
        </button>

        {/* Voice Quick Action */}
        <button
          onClick={handleRecordAudio}
          className={`w-full ${isRecording ? 'bg-red-600 animate-pulse' : hasAudio ? 'bg-purple-600' : 'bg-red-500'} hover:bg-red-600 text-white rounded-xl p-4 transition-all`}
        >
          <div className="flex items-center justify-center gap-3">
            <MicIcon sx={{ fontSize: 32 }} className={isRecording ? 'animate-pulse' : ''} />
            <div className="text-left flex-1">
              <p className="font-bold">
                {isRecording ? 'Grabando...' : hasAudio ? '✓ Audio Grabado' : 'Grabar Descripción'}
              </p>
              <p className="text-sm opacity-90">
                {isRecording ? 'Describe el problema' : 'Describe qué sucedió'}
              </p>
            </div>
          </div>
        </button>

        {/* Text Widget - Optional */}
        <div className="border-2 border-dashed border-gray-300 rounded-xl p-3">
          <div className="flex items-center gap-2 mb-2">
            <DescriptionIcon sx={{ fontSize: 20, color: '#6b7280' }} />
            <span className="text-sm font-bold text-gray-700">Detalles Adicionales (Opcional)</span>
          </div>
          <textarea
            placeholder="Agrega más información si lo deseas..."
            className="w-full border-0 bg-transparent text-sm text-gray-700 focus:outline-none min-h-16"
          />
        </div>
      </div>

      <button
        onClick={onSubmit}
        className="w-full bg-gradient-to-r from-yellow-500 to-orange-500 text-white rounded-xl p-4 font-bold text-lg shadow-lg flex items-center justify-center gap-2 hover:from-yellow-600 hover:to-orange-600 transition-all"
      >
        <FlashOnIcon sx={{ fontSize: 28 }} />
        Enviar Reporte de Emergencia
      </button>
    </div>
  );
}

function AIDiagnosisScreen({ progress }: { progress: number }) {
  return (
    <div className="p-4 flex flex-col items-center justify-center min-h-[600px]">
      <div className="bg-white rounded-2xl p-8 shadow-2xl text-center max-w-sm">
        <div className="bg-blue-100 rounded-full p-6 inline-block mb-4 animate-pulse">
          <HourglassEmptyIcon sx={{ fontSize: 72, color: '#2563eb' }} className="animate-spin" />
        </div>

        <h2 className="font-bold text-xl text-gray-800 mb-2">Diagnóstico Inteligente</h2>
        <p className="text-gray-600 mb-6">Analizando tu reporte con IA...</p>

        <div className="w-full bg-gray-200 rounded-full h-3 mb-4 overflow-hidden">
          <div
            className="bg-blue-600 h-full rounded-full transition-all duration-300"
            style={{ width: `${progress}%` }}
          />
        </div>

        <p className="text-sm text-gray-500">{progress}% completado</p>

        {progress > 60 && (
          <div className="mt-6 text-left space-y-2 animate-fade-in">
            <div className="flex items-center gap-2 text-sm">
              <CheckCircleIcon sx={{ fontSize: 18, color: '#16a34a' }} />
              <span>Ubicación verificada</span>
            </div>
            <div className="flex items-center gap-2 text-sm">
              <CheckCircleIcon sx={{ fontSize: 18, color: '#16a34a' }} />
              <span>Imágenes procesadas</span>
            </div>
            <div className="flex items-center gap-2 text-sm">
              <CheckCircleIcon sx={{ fontSize: 18, color: '#16a34a' }} />
              <span>Audio transcrito</span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

function TrackingScreen({ setScreen }: { setScreen: (screen: Screen) => void }) {
  return (
    <div className="p-4 space-y-4">
      <h2 className="font-bold text-gray-800">Seguimiento en Tiempo Real</h2>

      {/* AI Diagnosis Result */}
      <div className="bg-gradient-to-r from-blue-600 to-blue-700 text-white rounded-2xl p-4 shadow-lg">
        <div className="flex items-center gap-2 mb-2">
          <BarChartIcon sx={{ fontSize: 24 }} />
          <h3 className="font-bold">Diagnóstico Inteligente</h3>
        </div>
        <div className="space-y-2">
          <div className="bg-white/20 rounded-lg p-2">
            <p className="text-sm opacity-90">Tipo de Problema:</p>
            <p className="font-bold">Falla de Motor</p>
          </div>
          <div className="bg-white/20 rounded-lg p-2 flex items-center justify-between">
            <div>
              <p className="text-sm opacity-90">Prioridad:</p>
              <p className="font-bold text-yellow-300">ALTA</p>
            </div>
            <WarningIcon sx={{ fontSize: 28, color: '#fde047' }} />
          </div>
        </div>
      </div>

      {/* Status */}
      <div className="bg-white rounded-xl p-4 shadow-sm border border-gray-200">
        <div className="flex items-center gap-3 mb-4">
          <div className="bg-green-100 p-2 rounded-lg">
            <AccessTimeIcon sx={{ fontSize: 28, color: '#16a34a' }} />
          </div>
          <div>
            <p className="font-bold text-gray-800">Estado: En Proceso</p>
            <p className="text-sm text-gray-600">Técnico asignado</p>
          </div>
        </div>

        <div className="space-y-3">
          <div className="flex justify-between items-center pb-3 border-b">
            <span className="text-sm text-gray-600">Taller Asignado:</span>
            <span className="font-bold">AutoMaster Pro</span>
          </div>
          <div className="flex justify-between items-center pb-3 border-b">
            <span className="text-sm text-gray-600">Técnico:</span>
            <span className="font-bold">Carlos Méndez</span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-sm text-gray-600">ETA (Tiempo Estimado):</span>
            <span className="font-bold text-orange-600 text-xl">12 min</span>
          </div>
        </div>
      </div>

      {/* Map Placeholder */}
      <div className="bg-gray-100 rounded-xl h-48 flex items-center justify-center border border-gray-200">
        <div className="text-center">
          <LocationOnIcon sx={{ fontSize: 56, color: '#2563eb', marginX: 'auto', marginBottom: 1 }} />
          <p className="text-sm text-gray-600">Mapa en tiempo real</p>
          <p className="text-xs text-gray-500">Ubicación del técnico</p>
        </div>
      </div>

      {/* Communication */}
      <div className="grid grid-cols-2 gap-3">
        <button className="bg-green-600 text-white rounded-xl p-4 flex items-center justify-center gap-2 font-bold">
          <WhatsAppIcon sx={{ fontSize: 24 }} />
          WhatsApp
        </button>
        <button className="bg-blue-600 text-white rounded-xl p-4 flex items-center justify-center gap-2 font-bold">
          <PhoneIcon sx={{ fontSize: 24 }} />
          Llamar
        </button>
      </div>

      <button onClick={() => setScreen('payment')} className="w-full bg-purple-600 text-white rounded-xl p-4 font-bold">
        Ver Detalles de Pago
      </button>
    </div>
  );
}

function ProfileScreen() {
  return (
    <div className="p-4 space-y-4">
      <h2 className="font-bold text-gray-800">Mi Perfil</h2>

      <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200 text-center">
        <div className="bg-blue-100 w-24 h-24 rounded-full mx-auto mb-4 flex items-center justify-center">
          <PersonIcon sx={{ fontSize: 56, color: '#2563eb' }} />
        </div>
        <h3 className="font-bold text-xl">Juan Pérez</h3>
        <p className="text-gray-600">juan.perez@email.com</p>
        <p className="text-sm text-gray-500">+51 999 888 777</p>
      </div>

      <div className="space-y-2">
        <button className="w-full bg-white border border-gray-200 rounded-xl p-4 text-left font-medium hover:bg-gray-50">
          Editar Perfil
        </button>
        <button className="w-full bg-white border border-gray-200 rounded-xl p-4 text-left font-medium hover:bg-gray-50">
          Cambiar Contraseña
        </button>
        <button className="w-full bg-white border border-gray-200 rounded-xl p-4 text-left font-medium hover:bg-gray-50">
          Preferencias de Notificación
        </button>
        <button className="w-full bg-red-600 text-white rounded-xl p-4 text-left font-bold hover:bg-red-700">
          Cerrar Sesión
        </button>
      </div>
    </div>
  );
}

function PaymentScreen() {
  const [paymentMethod, setPaymentMethod] = useState<'card' | 'paypal' | 'cash' | null>(null);
  const [isPaying, setIsPaying] = useState(false);

  const handlePayment = (method: 'card' | 'paypal' | 'cash') => {
    setPaymentMethod(method);
    setIsPaying(true);
    setTimeout(() => {
      setIsPaying(false);
      alert(`Pago realizado con ${method === 'card' ? 'Tarjeta' : method === 'paypal' ? 'PayPal' : 'Efectivo'}`);
    }, 2000);
  };

  return (
    <div className="p-4 space-y-4">
      <h2 className="font-bold text-gray-800">Pagos y Facturas</h2>

      {/* Pending Payment Alert */}
      <div className="bg-red-50 border-2 border-red-400 rounded-xl p-4">
        <div className="flex items-center gap-3 mb-2">
          <WarningIcon sx={{ fontSize: 28, color: '#dc2626' }} />
          <div>
            <p className="font-bold text-red-800">Tienes un pago pendiente</p>
            <p className="text-sm text-red-600">Generado por el taller</p>
          </div>
        </div>
      </div>

      {/* Service Summary */}
      <div className="bg-white rounded-xl p-4 shadow-lg border-2 border-purple-300">
        <div className="flex items-center justify-between mb-3">
          <h3 className="font-bold text-purple-800">Servicio Completado</h3>
          <span className="bg-orange-100 text-orange-700 px-3 py-1 rounded-full text-xs font-bold">
            PENDIENTE DE PAGO
          </span>
        </div>

        <div className="space-y-2 text-sm mb-4">
          <div className="flex justify-between pb-2 border-b">
            <span className="text-gray-600">Servicio:</span>
            <span className="font-bold">Reparación de Motor</span>
          </div>
          <div className="flex justify-between pb-2 border-b">
            <span className="text-gray-600">Taller:</span>
            <span className="font-bold">AutoMaster Pro</span>
          </div>
          <div className="flex justify-between pb-2 border-b">
            <span className="text-gray-600">Fecha:</span>
            <span className="font-bold">20 Abr 2026</span>
          </div>
          <div className="flex justify-between pb-2 border-b">
            <span className="text-gray-600">Técnico:</span>
            <span className="font-bold">Carlos Méndez</span>
          </div>
          <div className="flex justify-between pb-2 border-b">
            <span className="text-gray-600">Costo del Servicio:</span>
            <span className="font-bold">S/ 250.00</span>
          </div>
          <div className="flex justify-between pb-2 border-b">
            <span className="text-gray-600">Comisión Plataforma (10%):</span>
            <span className="font-bold">S/ 25.00</span>
          </div>
          <div className="flex justify-between text-xl pt-3 bg-purple-50 -mx-2 px-2 py-2 rounded-lg">
            <span className="font-bold text-purple-800">Total a Pagar:</span>
            <span className="font-bold text-purple-600">S/ 275.00</span>
          </div>
        </div>

        <div className="bg-blue-50 rounded-lg p-3 mb-3">
          <p className="text-xs text-blue-800 mb-1 font-bold">Nota del Taller:</p>
          <p className="text-sm text-gray-700">
            Se realizó cambio de bujías y limpieza del sistema de inyección.
            El vehículo está listo para retiro.
          </p>
        </div>
      </div>

      {/* Payment Methods */}
      <div className="space-y-3">
        <h3 className="font-bold text-gray-800">Selecciona tu método de pago</h3>

        <button
          onClick={() => handlePayment('card')}
          disabled={isPaying}
          className="w-full bg-blue-600 hover:bg-blue-700 text-white rounded-xl p-4 flex items-center justify-center gap-2 font-bold transition-all disabled:opacity-50"
        >
          <CreditCardIcon sx={{ fontSize: 24 }} />
          {isPaying && paymentMethod === 'card' ? 'Procesando...' : 'Pagar con Tarjeta de Crédito/Débito'}
        </button>

        <button
          onClick={() => handlePayment('paypal')}
          disabled={isPaying}
          className="w-full bg-purple-600 hover:bg-purple-700 text-white rounded-xl p-4 font-bold transition-all disabled:opacity-50"
        >
          {isPaying && paymentMethod === 'paypal' ? 'Procesando...' : 'Pagar con PayPal'}
        </button>

        <button
          onClick={() => handlePayment('cash')}
          disabled={isPaying}
          className="w-full border-2 border-gray-300 hover:bg-gray-50 rounded-xl p-4 font-bold transition-all disabled:opacity-50"
        >
          {isPaying && paymentMethod === 'cash' ? 'Confirmando...' : 'Pagar en Efectivo al Taller'}
        </button>
      </div>

      {/* Payment Info */}
      <div className="bg-yellow-50 border border-yellow-300 rounded-xl p-3">
        <p className="text-xs text-yellow-800 font-bold mb-1">Información Importante:</p>
        <ul className="text-xs text-gray-700 space-y-1">
          <li>• Pago seguro procesado por Stripe/PayPal</li>
          <li>• Si pagas en efectivo, confirma con el taller</li>
          <li>• Recibirás tu factura por email</li>
          <li>• El taller recibirá el pago menos la comisión del 10%</li>
        </ul>
      </div>
    </div>
  );
}

function MyServicesScreen({ setScreen }: { setScreen: (screen: Screen) => void }) {
  const activeServices = [
    {
      id: 1,
      type: 'Falla de Motor',
      vehicle: 'Toyota Corolla - ABC-123',
      workshop: 'AutoMaster Pro',
      technician: 'Carlos Méndez',
      status: 'En Proceso',
      eta: '12 min',
      date: '2026-04-21',
      priority: 'ALTA'
    }
  ];

  const pendingPayment = [
    {
      id: 2,
      type: 'Reparación de Motor',
      vehicle: 'Toyota Corolla - ABC-123',
      workshop: 'AutoMaster Pro',
      technician: 'Carlos Méndez',
      status: 'Completado - Pendiente Pago',
      cost: 'S/ 275.00',
      date: '2026-04-20'
    }
  ];

  return (
    <div className="p-4 space-y-4">
      <h2 className="font-bold text-gray-800">Mis Atenciones</h2>

      {/* Active Services */}
      {activeServices.length > 0 && (
        <div className="space-y-3">
          <h3 className="text-sm font-bold text-blue-600 flex items-center gap-2">
            <PendingActionsIcon sx={{ fontSize: 18 }} />
            SERVICIOS ACTIVOS ({activeServices.length})
          </h3>

          {activeServices.map(service => (
            <div key={service.id} className="bg-white rounded-xl p-4 shadow-lg border-2 border-blue-400">
              <div className="flex justify-between items-start mb-3">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-1">
                    <WarningIcon sx={{ fontSize: 20, color: '#dc2626' }} />
                    <p className="font-bold text-gray-800">{service.type}</p>
                  </div>
                  <p className="text-xs text-gray-600 mb-1">{service.vehicle}</p>
                  <p className="text-xs text-gray-500">{service.date}</p>
                </div>
                <span className={`px-3 py-1 rounded-full text-xs font-bold ${
                  service.priority === 'ALTA' ? 'bg-red-100 text-red-700' :
                  service.priority === 'MEDIA' ? 'bg-yellow-100 text-yellow-700' :
                  'bg-green-100 text-green-700'
                }`}>
                  {service.priority}
                </span>
              </div>

              <div className="bg-blue-50 rounded-lg p-3 mb-3 space-y-1">
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600">Taller:</span>
                  <span className="font-bold">{service.workshop}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600">Técnico:</span>
                  <span className="font-bold">{service.technician}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600">ETA:</span>
                  <span className="font-bold text-orange-600">{service.eta}</span>
                </div>
              </div>

              <div className="flex items-center gap-2 mb-3">
                <div className="flex-1 bg-blue-100 rounded-lg px-3 py-2 text-center">
                  <p className="text-xs text-blue-600 font-bold">{service.status}</p>
                </div>
              </div>

              <div className="grid grid-cols-3 gap-2">
                <button onClick={() => setScreen('tracking')} className="bg-blue-600 text-white rounded-lg p-2 text-xs font-bold flex items-center justify-center gap-1">
                  <LocationOnIcon sx={{ fontSize: 16 }} />
                  Rastrear
                </button>
                <button className="bg-green-600 text-white rounded-lg p-2 text-xs font-bold flex items-center justify-center gap-1">
                  <WhatsAppIcon sx={{ fontSize: 16 }} />
                  Chat
                </button>
                <button className="border-2 border-blue-600 text-blue-600 rounded-lg p-2 text-xs font-bold flex items-center justify-center gap-1">
                  <PhoneIcon sx={{ fontSize: 16 }} />
                  Llamar
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Pending Payment */}
      {pendingPayment.length > 0 && (
        <div className="space-y-3">
          <h3 className="text-sm font-bold text-orange-600 flex items-center gap-2">
            <PaymentIcon sx={{ fontSize: 18 }} />
            PENDIENTES DE PAGO ({pendingPayment.length})
          </h3>

          {pendingPayment.map(service => (
            <div key={service.id} className="bg-white rounded-xl p-4 shadow-lg border-2 border-orange-400">
              <div className="flex justify-between items-start mb-3">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-1">
                    <CheckCircleIcon sx={{ fontSize: 20, color: '#16a34a' }} />
                    <p className="font-bold text-gray-800">{service.type}</p>
                  </div>
                  <p className="text-xs text-gray-600 mb-1">{service.vehicle}</p>
                  <p className="text-xs text-gray-500">{service.date}</p>
                </div>
                <span className="bg-orange-100 text-orange-700 px-3 py-1 rounded-full text-xs font-bold">
                  PAGO PENDIENTE
                </span>
              </div>

              <div className="bg-orange-50 rounded-lg p-3 mb-3 space-y-1">
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600">Taller:</span>
                  <span className="font-bold">{service.workshop}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600">Técnico:</span>
                  <span className="font-bold">{service.technician}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600">Total a Pagar:</span>
                  <span className="font-bold text-purple-600 text-lg">{service.cost}</span>
                </div>
              </div>

              <div className="flex items-center gap-2 mb-3">
                <div className="flex-1 bg-green-100 rounded-lg px-3 py-2 text-center">
                  <p className="text-xs text-green-700 font-bold">Servicio Completado</p>
                </div>
              </div>

              <button onClick={() => setScreen('payment')} className="w-full bg-gradient-to-r from-purple-600 to-orange-600 text-white rounded-lg p-3 font-bold flex items-center justify-center gap-2">
                <CreditCardIcon sx={{ fontSize: 20 }} />
                Pagar Ahora
              </button>
            </div>
          ))}
        </div>
      )}

      {/* Empty State */}
      {activeServices.length === 0 && pendingPayment.length === 0 && (
        <div className="bg-gray-50 rounded-xl p-8 text-center">
          <BuildIcon sx={{ fontSize: 64, color: '#9ca3af', marginX: 'auto', marginBottom: 2 }} />
          <p className="font-bold text-gray-600 mb-2">No tienes servicios activos</p>
          <p className="text-sm text-gray-500 mb-4">Cuando reportes una emergencia, aparecerá aquí</p>
          <button onClick={() => setScreen('report')} className="bg-orange-500 text-white px-6 py-2 rounded-lg font-bold">
            Reportar Incidente
          </button>
        </div>
      )}
    </div>
  );
}

function HistoryScreen() {
  const history = [
    { id: 1, date: '2026-04-18', type: 'Llanta Pinchada', status: 'Completado', cost: 'S/ 80', workshop: 'Taller Express' },
    { id: 2, date: '2026-04-10', type: 'Batería Descargada', status: 'Completado', cost: 'S/ 120', workshop: 'AutoService' },
    { id: 3, date: '2026-03-28', type: 'Cambio de Aceite', status: 'Completado', cost: 'S/ 95', workshop: 'MecaniExpress' }
  ];

  return (
    <div className="p-4 space-y-4">
      <h2 className="font-bold text-gray-800">Historial de Servicios</h2>
      <p className="text-sm text-gray-600">Servicios completados y pagados</p>

      <div className="space-y-3">
        {history.map(item => (
          <div key={item.id} className="bg-white rounded-xl p-4 shadow-sm border border-gray-200">
            <div className="flex justify-between items-start mb-2">
              <div>
                <p className="font-bold text-gray-800">{item.type}</p>
                <p className="text-xs text-gray-600">{item.workshop}</p>
                <p className="text-xs text-gray-500">{item.date}</p>
              </div>
              <span className="bg-green-100 text-green-700 px-3 py-1 rounded-full text-xs font-bold">
                {item.status}
              </span>
            </div>
            <div className="flex justify-between items-center pt-2 border-t">
              <span className="text-sm text-gray-600">Pagado:</span>
              <span className="font-bold text-purple-600">{item.cost}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
