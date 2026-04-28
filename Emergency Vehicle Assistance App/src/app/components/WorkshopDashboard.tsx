import { useState } from 'react';
import DashboardIcon from '@mui/icons-material/Dashboard';
import WarningIcon from '@mui/icons-material/Warning';
import AttachMoneyIcon from '@mui/icons-material/AttachMoney';
import BuildIcon from '@mui/icons-material/Build';
import PeopleIcon from '@mui/icons-material/People';
import SettingsIcon from '@mui/icons-material/Settings';
import DescriptionIcon from '@mui/icons-material/Description';
import LogoutIcon from '@mui/icons-material/Logout';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import CancelIcon from '@mui/icons-material/Cancel';
import AccessTimeIcon from '@mui/icons-material/AccessTime';
import LocationOnIcon from '@mui/icons-material/LocationOn';
import PhoneIcon from '@mui/icons-material/Phone';
import WhatsAppIcon from '@mui/icons-material/WhatsApp';
import DownloadIcon from '@mui/icons-material/Download';
import BarChartIcon from '@mui/icons-material/BarChart';
import SmartToyIcon from '@mui/icons-material/SmartToy';
import ImageIcon from '@mui/icons-material/Image';
import RadioIcon from '@mui/icons-material/Radio';
import AssignmentTurnedInIcon from '@mui/icons-material/AssignmentTurnedIn';
import ReceiptIcon from '@mui/icons-material/Receipt';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import TrendingDownIcon from '@mui/icons-material/TrendingDown';
import LocalShippingIcon from '@mui/icons-material/LocalShipping';
import StarIcon from '@mui/icons-material/Star';
import SpeedIcon from '@mui/icons-material/Speed';
import CalendarTodayIcon from '@mui/icons-material/CalendarToday';

type WorkshopView = 'dashboard' | 'requests' | 'technicians' | 'users' | 'logs' | 'settings';

export function WorkshopDashboard() {
  const [currentView, setCurrentView] = useState<WorkshopView>('dashboard');
  const [selectedRequest, setSelectedRequest] = useState<number | null>(null);

  return (
    <div className="w-full h-[800px] bg-gray-100 flex overflow-hidden">
      {/* Sidebar */}
      <div className="w-64 bg-slate-800 text-white flex flex-col">
        {/* Logo */}
        <div className="p-6 border-b border-slate-700">
          <div className="flex items-center gap-2">
            <BuildIcon sx={{ fontSize: 36, color: '#60a5fa' }} />
            <span className="font-bold text-xl">Taller Pro</span>
          </div>
        </div>

        {/* User Info */}
        <div className="p-4 border-b border-slate-700">
          <div className="flex items-center gap-3">
            <div className="bg-blue-600 w-10 h-10 rounded-full flex items-center justify-center font-bold">
              A
            </div>
            <div>
              <p className="font-bold text-sm">Administrador</p>
              <p className="text-xs text-gray-400">AutoMaster Pro</p>
            </div>
          </div>
        </div>

        {/* Navigation */}
        <nav className="flex-1 p-4">
          <div className="space-y-1">
            <p className="text-xs text-gray-400 uppercase tracking-wide mb-2">Operaciones</p>

            <button
              onClick={() => setCurrentView('dashboard')}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                currentView === 'dashboard' ? 'bg-blue-600' : 'hover:bg-slate-700'
              }`}
            >
              <DashboardIcon sx={{ fontSize: 24 }} />
              <span>Dashboard</span>
            </button>

            <button
              onClick={() => setCurrentView('requests')}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                currentView === 'requests' ? 'bg-blue-600' : 'hover:bg-slate-700'
              }`}
            >
              <WarningIcon sx={{ fontSize: 24 }} />
              <span>Emergencias</span>
            </button>

            <button
              onClick={() => setCurrentView('technicians')}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                currentView === 'technicians' ? 'bg-blue-600' : 'hover:bg-slate-700'
              }`}
            >
              <BuildIcon sx={{ fontSize: 24 }} />
              <span>Técnicos</span>
            </button>

            <p className="text-xs text-gray-400 uppercase tracking-wide mb-2 mt-6">Configuración</p>

            <button
              onClick={() => setCurrentView('users')}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                currentView === 'users' ? 'bg-blue-600' : 'hover:bg-slate-700'
              }`}
            >
              <PeopleIcon sx={{ fontSize: 24 }} />
              <span>Usuarios</span>
            </button>

            <button
              onClick={() => setCurrentView('logs')}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                currentView === 'logs' ? 'bg-blue-600' : 'hover:bg-slate-700'
              }`}
            >
              <DescriptionIcon sx={{ fontSize: 24 }} />
              <span>Bitácora</span>
            </button>

            <button
              onClick={() => setCurrentView('settings')}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                currentView === 'settings' ? 'bg-blue-600' : 'hover:bg-slate-700'
              }`}
            >
              <SettingsIcon sx={{ fontSize: 24 }} />
              <span>Configuración</span>
            </button>
          </div>
        </nav>

        {/* Logout */}
        <div className="p-4 border-t border-slate-700">
          <button className="w-full flex items-center gap-3 px-4 py-3 rounded-lg hover:bg-red-600 transition-colors">
            <LogoutIcon sx={{ fontSize: 24 }} />
            <span>Cerrar Sesión</span>
          </button>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Header */}
        <div className="bg-white border-b border-gray-200 px-8 py-4">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-2xl font-bold text-gray-800 flex items-center gap-2">
                <BuildIcon sx={{ fontSize: 28, color: '#2563eb' }} />
                Panel de Control - Taller Pro
              </h1>
            </div>
            <div className="text-right">
              <p className="text-sm text-blue-600">Bienvenido, Usuario</p>
              <p className="text-xs text-gray-500">20 de Abril, 2026</p>
            </div>
          </div>
        </div>

        {/* Content Area */}
        <div className="flex-1 overflow-y-auto p-8">
          {currentView === 'dashboard' && <DashboardView setView={setCurrentView} />}
          {currentView === 'requests' && <RequestsView selectedRequest={selectedRequest} setSelectedRequest={setSelectedRequest} />}
          {currentView === 'technicians' && <TechniciansView />}
          {currentView === 'users' && <UsersView />}
          {currentView === 'logs' && <LogsView />}
          {currentView === 'settings' && <SettingsView />}
        </div>
      </div>
    </div>
  );
}

function DashboardView({ setView }: { setView: (view: WorkshopView) => void }) {
  return (
    <div className="space-y-6">
      {/* Header Stats */}
      <div className="grid grid-cols-4 gap-6">
        {/* Solicitudes Activas */}
        <div className="bg-gradient-to-br from-orange-500 to-orange-600 rounded-xl p-6 shadow-lg text-white">
          <div className="flex items-center justify-between mb-4">
            <div className="bg-white/20 p-3 rounded-lg">
              <WarningIcon sx={{ fontSize: 32 }} />
            </div>
            <div className="text-right">
              <p className="text-sm opacity-90 mb-1">Solicitudes</p>
              <p className="text-4xl font-bold">8</p>
            </div>
          </div>
          <div className="flex items-center gap-1 text-sm">
            <TrendingUpIcon sx={{ fontSize: 16 }} />
            <span>+12% vs ayer</span>
          </div>
        </div>

        {/* Técnicos Activos */}
        <div className="bg-gradient-to-br from-green-500 to-green-600 rounded-xl p-6 shadow-lg text-white">
          <div className="flex items-center justify-between mb-4">
            <div className="bg-white/20 p-3 rounded-lg">
              <BuildIcon sx={{ fontSize: 32 }} />
            </div>
            <div className="text-right">
              <p className="text-sm opacity-90 mb-1">Técnicos Activos</p>
              <p className="text-4xl font-bold">12</p>
            </div>
          </div>
          <div className="flex items-center gap-1 text-sm">
            <span>de 15 totales</span>
          </div>
        </div>

        {/* Servicios Completados */}
        <div className="bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl p-6 shadow-lg text-white">
          <div className="flex items-center justify-between mb-4">
            <div className="bg-white/20 p-3 rounded-lg">
              <CheckCircleIcon sx={{ fontSize: 32 }} />
            </div>
            <div className="text-right">
              <p className="text-sm opacity-90 mb-1">Servicios Hoy</p>
              <p className="text-4xl font-bold">24</p>
            </div>
          </div>
          <div className="flex items-center gap-1 text-sm">
            <TrendingUpIcon sx={{ fontSize: 16 }} />
            <span>+8% vs ayer</span>
          </div>
        </div>

        {/* Ingresos */}
        <div className="bg-gradient-to-br from-purple-500 to-purple-600 rounded-xl p-6 shadow-lg text-white">
          <div className="flex items-center justify-between mb-4">
            <div className="bg-white/20 p-3 rounded-lg">
              <AttachMoneyIcon sx={{ fontSize: 32 }} />
            </div>
            <div className="text-right">
              <p className="text-sm opacity-90 mb-1">Ingresos Hoy</p>
              <p className="text-4xl font-bold">2,450</p>
            </div>
          </div>
          <div className="flex items-center gap-1 text-sm">
            <TrendingUpIcon sx={{ fontSize: 16 }} />
            <span>+15% vs ayer</span>
          </div>
        </div>
      </div>

      {/* Secondary Stats Row */}
      <div className="grid grid-cols-5 gap-4">
        <div className="bg-white rounded-lg p-4 shadow-sm border border-gray-200">
          <div className="flex items-center gap-3">
            <div className="bg-blue-100 p-2 rounded-lg">
              <SpeedIcon sx={{ fontSize: 24, color: '#2563eb' }} />
            </div>
            <div>
              <p className="text-xs text-gray-600">Tiempo Promedio</p>
              <p className="font-bold text-gray-800">18 min</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg p-4 shadow-sm border border-gray-200">
          <div className="flex items-center gap-3">
            <div className="bg-yellow-100 p-2 rounded-lg">
              <StarIcon sx={{ fontSize: 24, color: '#eab308' }} />
            </div>
            <div>
              <p className="text-xs text-gray-600">Calificación</p>
              <p className="font-bold text-gray-800">4.8/5.0</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg p-4 shadow-sm border border-gray-200">
          <div className="flex items-center gap-3">
            <div className="bg-green-100 p-2 rounded-lg">
              <LocalShippingIcon sx={{ fontSize: 24, color: '#16a34a' }} />
            </div>
            <div>
              <p className="text-xs text-gray-600">En Ruta</p>
              <p className="font-bold text-gray-800">5</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg p-4 shadow-sm border border-gray-200">
          <div className="flex items-center gap-3">
            <div className="bg-orange-100 p-2 rounded-lg">
              <AccessTimeIcon sx={{ fontSize: 24, color: '#ea580c' }} />
            </div>
            <div>
              <p className="text-xs text-gray-600">Pendientes</p>
              <p className="font-bold text-gray-800">3</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg p-4 shadow-sm border border-gray-200">
          <div className="flex items-center gap-3">
            <div className="bg-purple-100 p-2 rounded-lg">
              <ReceiptIcon sx={{ fontSize: 24, color: '#9333ea' }} />
            </div>
            <div>
              <p className="text-xs text-gray-600">Pagos Pend.</p>
              <p className="font-bold text-gray-800">S/ 825</p>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-3 gap-6">
        {/* Left Column - Recent Requests */}
        <div className="col-span-2 space-y-6">
          {/* Recent Requests */}
          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
            <div className="flex justify-between items-center mb-4">
              <h2 className="font-bold text-xl flex items-center gap-2">
                <WarningIcon sx={{ fontSize: 24, color: '#ea580c' }} />
                Solicitudes Recientes
              </h2>
              <button onClick={() => setView('requests')} className="bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-bold hover:bg-blue-700">
                Ver todas →
              </button>
            </div>

            <div className="space-y-3">
              {[
                { id: 1, client: 'Juan Pérez', issue: 'Falla de Motor', priority: 'ALTA', time: '5 min', status: 'Pendiente', location: '2.3 km' },
                { id: 2, client: 'María López', issue: 'Llanta Pinchada', priority: 'MEDIA', time: '12 min', status: 'En Proceso', location: '1.8 km' },
                { id: 3, client: 'Carlos Ruiz', issue: 'Batería Descargada', priority: 'BAJA', time: '20 min', status: 'En Proceso', location: '3.5 km' }
              ].map(request => (
                <div key={request.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-all border-l-4 border-l-blue-500 cursor-pointer">
                  <div className="flex items-center gap-4">
                    <div className="bg-blue-100 p-2 rounded-lg">
                      <WarningIcon sx={{ fontSize: 24, color: '#2563eb' }} />
                    </div>
                    <div>
                      <p className="font-bold text-gray-800">{request.client}</p>
                      <p className="text-sm text-gray-600">{request.issue}</p>
                      <div className="flex items-center gap-2 mt-1">
                        <LocationOnIcon sx={{ fontSize: 14, color: '#6b7280' }} />
                        <span className="text-xs text-gray-500">{request.location}</span>
                      </div>
                    </div>
                  </div>
                  <div className="flex items-center gap-3">
                    <span className={`px-3 py-1 rounded-full text-xs font-bold ${
                      request.priority === 'ALTA' ? 'bg-red-100 text-red-700' :
                      request.priority === 'MEDIA' ? 'bg-yellow-100 text-yellow-700' :
                      'bg-green-100 text-green-700'
                    }`}>
                      {request.priority}
                    </span>
                    <div className="text-right">
                      <p className="text-xs text-gray-500">{request.time}</p>
                      <span className={`text-xs font-bold ${
                        request.status === 'Pendiente' ? 'text-orange-600' : 'text-blue-600'
                      }`}>
                        {request.status}
                      </span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Performance Chart */}
          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
            <h3 className="font-bold text-lg mb-4 flex items-center gap-2">
              <BarChartIcon sx={{ fontSize: 24, color: '#2563eb' }} />
              Servicios Esta Semana
            </h3>
            <div className="space-y-3">
              {[
                { day: 'Lunes', services: 18, revenue: 1850 },
                { day: 'Martes', services: 22, revenue: 2340 },
                { day: 'Miércoles', services: 20, revenue: 2100 },
                { day: 'Jueves', services: 25, revenue: 2650 },
                { day: 'Viernes', services: 24, revenue: 2450 },
                { day: 'Sábado', services: 15, revenue: 1520 },
                { day: 'Domingo', services: 8, revenue: 890 }
              ].map((item, index) => (
                <div key={index} className="flex items-center gap-4">
                  <span className="text-sm font-bold text-gray-700 w-24">{item.day}</span>
                  <div className="flex-1 bg-gray-200 rounded-full h-6 overflow-hidden">
                    <div
                      className="bg-gradient-to-r from-blue-500 to-purple-500 h-full rounded-full flex items-center justify-end pr-2"
                      style={{ width: `${(item.services / 25) * 100}%` }}
                    >
                      <span className="text-xs font-bold text-white">{item.services}</span>
                    </div>
                  </div>
                  <span className="text-sm font-bold text-purple-600 w-20">S/ {item.revenue}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Right Column - Quick Info */}
        <div className="space-y-6">
          {/* Technicians Status */}
          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
            <h3 className="font-bold text-lg mb-4 flex items-center gap-2">
              <BuildIcon sx={{ fontSize: 24, color: '#16a34a' }} />
              Estado de Técnicos
            </h3>
            <div className="space-y-3">
              {[
                { name: 'Carlos Méndez', status: 'Ocupado', service: 'Servicio #1234' },
                { name: 'Luis Torres', status: 'Ocupado', service: 'Servicio #1235' },
                { name: 'Pedro Sánchez', status: 'Disponible', service: '-' },
                { name: 'Miguel Ramos', status: 'Disponible', service: '-' }
              ].map((tech, index) => (
                <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div className="flex items-center gap-3">
                    <div className={`w-3 h-3 rounded-full ${tech.status === 'Disponible' ? 'bg-green-500' : 'bg-orange-500'}`} />
                    <div>
                      <p className="text-sm font-bold text-gray-800">{tech.name}</p>
                      <p className="text-xs text-gray-500">{tech.service}</p>
                    </div>
                  </div>
                  <span className={`text-xs font-bold ${tech.status === 'Disponible' ? 'text-green-600' : 'text-orange-600'}`}>
                    {tech.status}
                  </span>
                </div>
              ))}
            </div>
            <button onClick={() => setView('technicians')} className="w-full mt-4 border-2 border-blue-600 text-blue-600 rounded-lg p-2 text-sm font-bold hover:bg-blue-50">
              Ver Todos
            </button>
          </div>

          {/* AI Analytics */}
          <div className="bg-gradient-to-br from-blue-600 to-purple-600 rounded-xl p-6 shadow-lg text-white">
            <h3 className="font-bold text-lg mb-4 flex items-center gap-2">
              <SmartToyIcon sx={{ fontSize: 24 }} />
              Análisis IA
            </h3>
            <div className="space-y-3">
              <div className="bg-white/20 rounded-lg p-3">
                <p className="text-sm opacity-90 mb-1">Problemas Más Frecuentes</p>
                <p className="font-bold">1. Falla de Motor (35%)</p>
                <p className="font-bold">2. Llanta Pinchada (28%)</p>
                <p className="font-bold">3. Batería (22%)</p>
              </div>
              <div className="bg-white/20 rounded-lg p-3">
                <p className="text-sm opacity-90 mb-1">Precisión del Diagnóstico</p>
                <p className="text-2xl font-bold">94.2%</p>
              </div>
            </div>
          </div>

          {/* Quick Stats */}
          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
            <h3 className="font-bold text-lg mb-4 flex items-center gap-2">
              <CalendarTodayIcon sx={{ fontSize: 24, color: '#6b7280' }} />
              Resumen Mensual
            </h3>
            <div className="space-y-3">
              <div className="flex justify-between items-center pb-2 border-b">
                <span className="text-sm text-gray-600">Servicios Totales:</span>
                <span className="font-bold text-gray-800">487</span>
              </div>
              <div className="flex justify-between items-center pb-2 border-b">
                <span className="text-sm text-gray-600">Ingresos Brutos:</span>
                <span className="font-bold text-green-600">S/ 48,750</span>
              </div>
              <div className="flex justify-between items-center pb-2 border-b">
                <span className="text-sm text-gray-600">Comisiones:</span>
                <span className="font-bold text-purple-600">S/ 4,875</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-600">Ingresos Netos:</span>
                <span className="font-bold text-blue-600 text-lg">S/ 43,875</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function RequestsView({ selectedRequest, setSelectedRequest }: { selectedRequest: number | null; setSelectedRequest: (id: number | null) => void }) {
  const [serviceStatus, setServiceStatus] = useState<string>('');
  const [showInvoiceForm, setShowInvoiceForm] = useState(false);
  const [invoiceData, setInvoiceData] = useState({
    serviceCost: '',
    description: '',
    partsUsed: ''
  });

  const requests = [
    {
      id: 1,
      client: 'Juan Pérez',
      phone: '+51 999 888 777',
      vehicle: 'Toyota Corolla - ABC-123',
      issue: 'Falla de Motor',
      aiSummary: 'Motor no enciende. Posible problema eléctrico o de combustible. Batería en buen estado según imagen.',
      priority: 'ALTA',
      status: 'Pendiente',
      location: 'Av. Arequipa 1234, Lima',
      distance: '2.3 km',
      time: '5 min ago',
      images: true,
      audio: true
    },
    {
      id: 2,
      client: 'María López',
      phone: '+51 987 654 321',
      vehicle: 'Honda Civic - XYZ-789',
      issue: 'Llanta Pinchada',
      aiSummary: 'Llanta delantera izquierda pinchada. Cliente tiene llanta de repuesto disponible.',
      priority: 'MEDIA',
      status: 'En Proceso',
      location: 'Jr. Libertad 567, Lima',
      distance: '1.8 km',
      time: '12 min ago',
      images: true,
      audio: false
    }
  ];

  const selected = requests.find(r => r.id === selectedRequest);

  const handleUpdateStatus = (status: string) => {
    setServiceStatus(status);
    alert(`Estado actualizado a: ${status}`);
  };

  const handleGenerateInvoice = () => {
    const cost = parseFloat(invoiceData.serviceCost);
    const commission = cost * 0.10;
    const total = cost + commission;

    alert(`Factura generada:\nCosto: S/ ${cost.toFixed(2)}\nComisión (10%): S/ ${commission.toFixed(2)}\nTotal: S/ ${total.toFixed(2)}\n\nLa deuda fue enviada al cliente.`);
    setShowInvoiceForm(false);
    setInvoiceData({ serviceCost: '', description: '', partsUsed: '' });
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="font-bold text-2xl">Solicitudes de Emergencia</h2>
        <div className="flex gap-3">
          <select className="border border-gray-300 rounded-lg px-4 py-2">
            <option>Todas las prioridades</option>
            <option>Alta</option>
            <option>Media</option>
            <option>Baja</option>
          </select>
          <select className="border border-gray-300 rounded-lg px-4 py-2">
            <option>Todos los estados</option>
            <option>Pendiente</option>
            <option>En Proceso</option>
            <option>Completado</option>
          </select>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-6">
        {/* Requests List */}
        <div className="space-y-3">
          {requests.map(request => (
            <div
              key={request.id}
              onClick={() => setSelectedRequest(request.id)}
              className={`bg-white rounded-xl p-4 shadow-sm border-2 cursor-pointer transition-all ${
                selectedRequest === request.id ? 'border-blue-500' : 'border-gray-200 hover:border-gray-300'
              }`}
            >
              <div className="flex justify-between items-start mb-3">
                <div>
                  <p className="font-bold text-gray-800">{request.client}</p>
                  <p className="text-sm text-gray-600">{request.vehicle}</p>
                </div>
                <span className={`px-3 py-1 rounded-full text-xs font-bold flex items-center gap-1 ${
                  request.priority === 'ALTA' ? 'bg-red-100 text-red-700' :
                  request.priority === 'MEDIA' ? 'bg-yellow-100 text-yellow-700' :
                  'bg-green-100 text-green-700'
                }`}>
                  <WarningIcon sx={{ fontSize: 14 }} />
                  {request.priority}
                </span>
              </div>

              <div className="bg-blue-50 rounded-lg p-3 mb-3">
                <div className="flex items-center gap-1 mb-1">
                  <BarChartIcon sx={{ fontSize: 14, color: '#2563eb' }} />
                  <p className="text-xs text-blue-600">Resumen IA:</p>
                </div>
                <p className="text-sm text-gray-700">{request.aiSummary}</p>
              </div>

              <div className="flex items-center gap-2 text-sm text-gray-600 mb-2">
                <LocationOnIcon sx={{ fontSize: 16 }} />
                <span>{request.location}</span>
                <span className="text-blue-600 font-bold">({request.distance})</span>
              </div>

              <div className="flex justify-between items-center">
                <div className="flex gap-2">
                  {request.images && (
                    <span className="bg-green-100 text-green-700 px-2 py-1 rounded text-xs flex items-center gap-1">
                      <ImageIcon sx={{ fontSize: 14 }} />
                      Fotos
                    </span>
                  )}
                  {request.audio && (
                    <span className="bg-purple-100 text-purple-700 px-2 py-1 rounded text-xs flex items-center gap-1">
                      <RadioIcon sx={{ fontSize: 14 }} />
                      Audio
                    </span>
                  )}
                </div>
                <span className="text-xs text-gray-500">{request.time}</span>
              </div>
            </div>
          ))}
        </div>

        {/* Request Detail */}
        <div>
          {selected ? (
            <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200 sticky top-0">
              <h3 className="font-bold text-xl mb-4">Detalle de Solicitud</h3>

              <div className="space-y-4">
                <div>
                  <p className="text-sm text-gray-600 mb-1">Cliente</p>
                  <p className="font-bold">{selected.client}</p>
                  <p className="text-sm text-gray-600">{selected.phone}</p>
                </div>

                <div>
                  <p className="text-sm text-gray-600 mb-1">Vehículo</p>
                  <p className="font-bold">{selected.vehicle}</p>
                </div>

                <div>
                  <p className="text-sm text-gray-600 mb-1">Problema Reportado</p>
                  <p className="font-bold text-orange-600">{selected.issue}</p>
                </div>

                <div className="bg-gradient-to-r from-blue-600 to-blue-700 text-white rounded-lg p-4">
                  <div className="flex items-center gap-2 mb-2">
                    <SmartToyIcon sx={{ fontSize: 20 }} />
                    <p className="text-sm font-bold">Diagnóstico IA:</p>
                  </div>
                  <p className="text-sm">{selected.aiSummary}</p>
                </div>

                <div>
                  <p className="text-sm text-gray-600 mb-1">Ubicación</p>
                  <p className="font-bold">{selected.location}</p>
                  <div className="bg-gray-100 rounded-lg h-32 mt-2 flex items-center justify-center">
                    <LocationOnIcon sx={{ fontSize: 36, color: '#2563eb' }} />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-3">
                  <button className="bg-green-600 text-white rounded-lg p-3 flex items-center justify-center gap-2 font-bold hover:bg-green-700">
                    <CheckCircleIcon sx={{ fontSize: 20 }} />
                    Aceptar
                  </button>
                  <button className="bg-red-600 text-white rounded-lg p-3 flex items-center justify-center gap-2 font-bold hover:bg-red-700">
                    <CancelIcon sx={{ fontSize: 20 }} />
                    Rechazar
                  </button>
                </div>

                <div className="grid grid-cols-2 gap-3">
                  <button className="border-2 border-green-600 text-green-700 rounded-lg p-3 flex items-center justify-center gap-2 font-bold hover:bg-green-50">
                    <WhatsAppIcon sx={{ fontSize: 20 }} />
                    WhatsApp
                  </button>
                  <button className="border-2 border-blue-600 text-blue-700 rounded-lg p-3 flex items-center justify-center gap-2 font-bold hover:bg-blue-50">
                    <PhoneIcon sx={{ fontSize: 20 }} />
                    Llamar
                  </button>
                </div>

                <button className="w-full bg-purple-600 text-white rounded-lg p-3 flex items-center justify-center gap-2 font-bold hover:bg-purple-700">
                  <DownloadIcon sx={{ fontSize: 20 }} />
                  Descargar Reporte PDF
                </button>

                {/* Update Service Status */}
                <div className="border-t pt-4">
                  <h4 className="font-bold mb-2 flex items-center gap-2">
                    <AssignmentTurnedInIcon sx={{ fontSize: 20 }} />
                    Actualizar Estado del Servicio
                  </h4>
                  <div className="grid grid-cols-2 gap-2 mb-3">
                    <button
                      onClick={() => handleUpdateStatus('En Ruta')}
                      className="bg-blue-100 text-blue-700 rounded-lg p-2 text-xs font-bold hover:bg-blue-200"
                    >
                      En Ruta
                    </button>
                    <button
                      onClick={() => handleUpdateStatus('En Sitio')}
                      className="bg-yellow-100 text-yellow-700 rounded-lg p-2 text-xs font-bold hover:bg-yellow-200"
                    >
                      En Sitio
                    </button>
                    <button
                      onClick={() => handleUpdateStatus('Trabajando')}
                      className="bg-orange-100 text-orange-700 rounded-lg p-2 text-xs font-bold hover:bg-orange-200"
                    >
                      Trabajando
                    </button>
                    <button
                      onClick={() => handleUpdateStatus('Completado')}
                      className="bg-green-100 text-green-700 rounded-lg p-2 text-xs font-bold hover:bg-green-200"
                    >
                      Completado
                    </button>
                  </div>
                  {serviceStatus && (
                    <p className="text-xs text-green-600 bg-green-50 p-2 rounded">
                      ✓ Estado actualizado: {serviceStatus}
                    </p>
                  )}
                </div>

                {/* Generate Invoice */}
                <div className="border-t pt-4">
                  <button
                    onClick={() => setShowInvoiceForm(!showInvoiceForm)}
                    className="w-full bg-gradient-to-r from-purple-600 to-orange-600 text-white rounded-lg p-3 flex items-center justify-center gap-2 font-bold hover:opacity-90"
                  >
                    <ReceiptIcon sx={{ fontSize: 20 }} />
                    {showInvoiceForm ? 'Cancelar Factura' : 'Generar Factura y Cobro'}
                  </button>

                  {showInvoiceForm && (
                    <div className="mt-3 space-y-3 bg-purple-50 p-3 rounded-lg">
                      <div>
                        <label className="text-xs font-bold text-gray-700 block mb-1">
                          Costo del Servicio (S/)
                        </label>
                        <input
                          type="number"
                          value={invoiceData.serviceCost}
                          onChange={(e) => setInvoiceData({...invoiceData, serviceCost: e.target.value})}
                          placeholder="250.00"
                          className="w-full border border-gray-300 rounded p-2 text-sm"
                        />
                      </div>

                      <div>
                        <label className="text-xs font-bold text-gray-700 block mb-1">
                          Descripción del Trabajo
                        </label>
                        <textarea
                          value={invoiceData.description}
                          onChange={(e) => setInvoiceData({...invoiceData, description: e.target.value})}
                          placeholder="Ej: Cambio de bujías, limpieza de inyectores..."
                          className="w-full border border-gray-300 rounded p-2 text-sm"
                          rows={2}
                        />
                      </div>

                      <div>
                        <label className="text-xs font-bold text-gray-700 block mb-1">
                          Repuestos Utilizados
                        </label>
                        <input
                          type="text"
                          value={invoiceData.partsUsed}
                          onChange={(e) => setInvoiceData({...invoiceData, partsUsed: e.target.value})}
                          placeholder="Ej: 4 bujías NGK, filtro de aire"
                          className="w-full border border-gray-300 rounded p-2 text-sm"
                        />
                      </div>

                      {invoiceData.serviceCost && (
                        <div className="bg-white rounded p-2 text-xs">
                          <div className="flex justify-between mb-1">
                            <span>Costo del Servicio:</span>
                            <span className="font-bold">S/ {parseFloat(invoiceData.serviceCost).toFixed(2)}</span>
                          </div>
                          <div className="flex justify-between mb-1">
                            <span>Comisión (10%):</span>
                            <span className="font-bold">S/ {(parseFloat(invoiceData.serviceCost) * 0.10).toFixed(2)}</span>
                          </div>
                          <div className="flex justify-between border-t pt-1 text-purple-600">
                            <span className="font-bold">Total al Cliente:</span>
                            <span className="font-bold">S/ {(parseFloat(invoiceData.serviceCost) * 1.10).toFixed(2)}</span>
                          </div>
                          <div className="flex justify-between text-green-600">
                            <span className="font-bold">Tú Recibes:</span>
                            <span className="font-bold">S/ {parseFloat(invoiceData.serviceCost).toFixed(2)}</span>
                          </div>
                        </div>
                      )}

                      <button
                        onClick={handleGenerateInvoice}
                        disabled={!invoiceData.serviceCost || !invoiceData.description}
                        className="w-full bg-green-600 text-white rounded-lg p-2 text-sm font-bold hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed"
                      >
                        Generar y Enviar al Cliente
                      </button>
                    </div>
                  )}
                </div>
              </div>
            </div>
          ) : (
            <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200 h-full flex items-center justify-center">
              <p className="text-gray-500">Selecciona una solicitud para ver los detalles</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

function TechniciansView() {
  const technicians = [
    { id: 1, name: 'Carlos Méndez', phone: '+51 999 111 222', status: 'Activo', assigned: 'Servicio #1234', specialty: 'Motor' },
    { id: 2, name: 'Luis Torres', phone: '+51 999 333 444', status: 'Activo', assigned: 'Servicio #1235', specialty: 'Llantas' },
    { id: 3, name: 'Pedro Sánchez', phone: '+51 999 555 666', status: 'Disponible', assigned: '-', specialty: 'Eléctrico' },
    { id: 4, name: 'Miguel Ramos', phone: '+51 999 777 888', status: 'Inactivo', assigned: '-', specialty: 'General' }
  ];

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="font-bold text-2xl">Gestión de Técnicos</h2>
        <button className="bg-blue-600 text-white px-6 py-3 rounded-lg font-bold hover:bg-blue-700">
          + Agregar Técnico
        </button>
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
        <table className="w-full">
          <thead className="bg-gray-50 border-b border-gray-200">
            <tr>
              <th className="text-left p-4 font-bold text-gray-700">Nombre</th>
              <th className="text-left p-4 font-bold text-gray-700">Teléfono</th>
              <th className="text-left p-4 font-bold text-gray-700">Especialidad</th>
              <th className="text-left p-4 font-bold text-gray-700">Estado</th>
              <th className="text-left p-4 font-bold text-gray-700">Asignado a</th>
              <th className="text-left p-4 font-bold text-gray-700">Acciones</th>
            </tr>
          </thead>
          <tbody>
            {technicians.map(tech => (
              <tr key={tech.id} className="border-b border-gray-100 hover:bg-gray-50">
                <td className="p-4 font-bold text-gray-800">{tech.name}</td>
                <td className="p-4 text-gray-600">{tech.phone}</td>
                <td className="p-4 text-gray-600">{tech.specialty}</td>
                <td className="p-4">
                  <span className={`px-3 py-1 rounded-full text-xs font-bold ${
                    tech.status === 'Activo' ? 'bg-blue-100 text-blue-700' :
                    tech.status === 'Disponible' ? 'bg-green-100 text-green-700' :
                    'bg-gray-100 text-gray-700'
                  }`}>
                    {tech.status}
                  </span>
                </td>
                <td className="p-4 text-gray-600">{tech.assigned}</td>
                <td className="p-4">
                  <button className="text-blue-600 hover:underline mr-3">Editar</button>
                  <button className="text-red-600 hover:underline">Eliminar</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function UsersView() {
  const users = [
    { id: 1, name: 'Juan Pérez', email: 'juan@email.com', phone: '+51 999 888 777', role: 'Cliente', registered: '2026-01-15' },
    { id: 2, name: 'María López', email: 'maria@email.com', phone: '+51 987 654 321', role: 'Cliente', registered: '2026-02-20' },
    { id: 3, name: 'AutoMaster Pro', email: 'admin@automaster.com', phone: '+51 999 000 111', role: 'Taller', registered: '2025-12-01' }
  ];

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="font-bold text-2xl">Gestión de Usuarios</h2>
        <input
          type="search"
          placeholder="Buscar usuarios..."
          className="border border-gray-300 rounded-lg px-4 py-2 w-64"
        />
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
        <table className="w-full">
          <thead className="bg-gray-50 border-b border-gray-200">
            <tr>
              <th className="text-left p-4 font-bold text-gray-700">Nombre</th>
              <th className="text-left p-4 font-bold text-gray-700">Email</th>
              <th className="text-left p-4 font-bold text-gray-700">Teléfono</th>
              <th className="text-left p-4 font-bold text-gray-700">Rol</th>
              <th className="text-left p-4 font-bold text-gray-700">Fecha Registro</th>
              <th className="text-left p-4 font-bold text-gray-700">Acciones</th>
            </tr>
          </thead>
          <tbody>
            {users.map(user => (
              <tr key={user.id} className="border-b border-gray-100 hover:bg-gray-50">
                <td className="p-4 font-bold text-gray-800">{user.name}</td>
                <td className="p-4 text-gray-600">{user.email}</td>
                <td className="p-4 text-gray-600">{user.phone}</td>
                <td className="p-4">
                  <span className={`px-3 py-1 rounded-full text-xs font-bold ${
                    user.role === 'Taller' ? 'bg-purple-100 text-purple-700' : 'bg-blue-100 text-blue-700'
                  }`}>
                    {user.role}
                  </span>
                </td>
                <td className="p-4 text-gray-600">{user.registered}</td>
                <td className="p-4">
                  <button className="text-blue-600 hover:underline mr-3">Ver</button>
                  <button className="text-red-600 hover:underline">Desactivar</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function LogsView() {
  const logs = [
    { id: 1, timestamp: '2026-04-20 14:35:22', user: 'admin@automaster.com', action: 'Aceptó solicitud de emergencia', type: 'success', details: 'Solicitud #1234' },
    { id: 2, timestamp: '2026-04-20 14:22:11', user: 'juan@email.com', action: 'Reportó nueva emergencia', type: 'info', details: 'Falla de Motor' },
    { id: 3, timestamp: '2026-04-20 14:15:45', user: 'admin@automaster.com', action: 'Asignó técnico a servicio', type: 'success', details: 'Carlos Méndez → Servicio #1233' },
    { id: 4, timestamp: '2026-04-20 13:58:30', user: 'maria@email.com', action: 'Completó pago de servicio', type: 'success', details: 'S/ 80.00' },
    { id: 5, timestamp: '2026-04-20 13:45:12', user: 'system', action: 'Error en clasificación IA', type: 'error', details: 'Audio corrupto - Solicitud #1230' }
  ];

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="font-bold text-2xl">Bitácora de Auditoría</h2>
        <div className="flex gap-3">
          <select className="border border-gray-300 rounded-lg px-4 py-2">
            <option>Todos los tipos</option>
            <option>Success</option>
            <option>Info</option>
            <option>Error</option>
          </select>
          <input type="date" className="border border-gray-300 rounded-lg px-4 py-2" />
        </div>
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50 border-b border-gray-200">
              <tr>
                <th className="text-left p-4 font-bold text-gray-700">Timestamp</th>
                <th className="text-left p-4 font-bold text-gray-700">Usuario</th>
                <th className="text-left p-4 font-bold text-gray-700">Acción</th>
                <th className="text-left p-4 font-bold text-gray-700">Detalles</th>
                <th className="text-left p-4 font-bold text-gray-700">Tipo</th>
              </tr>
            </thead>
            <tbody>
              {logs.map(log => (
                <tr key={log.id} className="border-b border-gray-100 hover:bg-gray-50">
                  <td className="p-4 text-sm text-gray-600 font-mono">{log.timestamp}</td>
                  <td className="p-4 text-sm text-gray-800">{log.user}</td>
                  <td className="p-4 text-sm text-gray-800">{log.action}</td>
                  <td className="p-4 text-sm text-gray-600">{log.details}</td>
                  <td className="p-4">
                    <span className={`px-3 py-1 rounded-full text-xs font-bold ${
                      log.type === 'success' ? 'bg-green-100 text-green-700' :
                      log.type === 'error' ? 'bg-red-100 text-red-700' :
                      'bg-blue-100 text-blue-700'
                    }`}>
                      {log.type.toUpperCase()}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

function SettingsView() {
  return (
    <div className="space-y-6">
      <h2 className="font-bold text-2xl">Configuración del Sistema</h2>

      <div className="grid grid-cols-2 gap-6">
        <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
          <h3 className="font-bold mb-4">Configuración del Taller</h3>
          <div className="space-y-3">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Nombre del Taller</label>
              <input type="text" defaultValue="AutoMaster Pro" className="w-full border border-gray-300 rounded-lg p-2" />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Teléfono</label>
              <input type="text" defaultValue="+51 999 000 111" className="w-full border border-gray-300 rounded-lg p-2" />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Dirección</label>
              <input type="text" defaultValue="Av. Principal 123, Lima" className="w-full border border-gray-300 rounded-lg p-2" />
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
          <h3 className="font-bold mb-4">Configuración de Pagos</h3>
          <div className="space-y-3">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Comisión de Plataforma (%)</label>
              <input type="number" defaultValue="10" className="w-full border border-gray-300 rounded-lg p-2" />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Métodos de Pago Aceptados</label>
              <div className="space-y-2">
                <label className="flex items-center gap-2">
                  <input type="checkbox" defaultChecked className="rounded" />
                  <span className="text-sm">Tarjeta de Crédito/Débito</span>
                </label>
                <label className="flex items-center gap-2">
                  <input type="checkbox" defaultChecked className="rounded" />
                  <span className="text-sm">PayPal</span>
                </label>
                <label className="flex items-center gap-2">
                  <input type="checkbox" defaultChecked className="rounded" />
                  <span className="text-sm">Efectivo</span>
                </label>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
          <h3 className="font-bold mb-4">Notificaciones</h3>
          <div className="space-y-2">
            <label className="flex items-center gap-2">
              <input type="checkbox" defaultChecked className="rounded" />
              <span className="text-sm">Notificaciones Push</span>
            </label>
            <label className="flex items-center gap-2">
              <input type="checkbox" defaultChecked className="rounded" />
              <span className="text-sm">Notificaciones por Email</span>
            </label>
            <label className="flex items-center gap-2">
              <input type="checkbox" defaultChecked className="rounded" />
              <span className="text-sm">Notificaciones de WhatsApp</span>
            </label>
          </div>
        </div>

        <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
          <h3 className="font-bold mb-4">Configuración IA</h3>
          <div className="space-y-3">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Modelo de Clasificación</label>
              <select className="w-full border border-gray-300 rounded-lg p-2">
                <option>GPT-4 Vision</option>
                <option>Claude 4 Vision</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Umbral de Confianza (%)</label>
              <input type="number" defaultValue="85" className="w-full border border-gray-300 rounded-lg p-2" />
            </div>
          </div>
        </div>
      </div>

      <div className="flex justify-end gap-3">
        <button className="border border-gray-300 px-6 py-3 rounded-lg font-bold hover:bg-gray-50">
          Cancelar
        </button>
        <button className="bg-blue-600 text-white px-6 py-3 rounded-lg font-bold hover:bg-blue-700">
          Guardar Cambios
        </button>
      </div>
    </div>
  );
}
