import { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs.jsx'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select.jsx'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table.jsx'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, BarChart, Bar } from 'recharts'
import { Search, TrendingUp, TrendingDown, Activity, DollarSign, Package, AlertTriangle } from 'lucide-react'
import './App.css'

// Mock data for development
const mockItems = [
  { type_id: 34, name: "Tritanium", group_id: 18, volume: 0.01 },
  { type_id: 35, name: "Pyerite", group_id: 18, volume: 0.01 },
  { type_id: 36, name: "Mexallon", group_id: 18, volume: 0.01 },
  { type_id: 37, name: "Isogen", group_id: 18, volume: 0.01 },
  { type_id: 38, name: "Nocxium", group_id: 18, volume: 0.01 },
]

const mockRegions = [
  { region_id: 10000002, name: "The Forge (Jita)" },
  { region_id: 10000043, name: "Domain (Amarr)" },
  { region_id: 10000032, name: "Sinq Laison (Dodixie)" },
  { region_id: 10000030, name: "Heimatar (Rens)" },
  { region_id: 10000042, name: "Metropolis (Hek)" },
]

const mockArbitrageData = [
  {
    item: { name: "Tritanium", type_id: 34 },
    buy_region: { name: "The Forge (Jita)" },
    sell_region: { name: "Domain (Amarr)" },
    buy_price: 5.50,
    sell_price: 4.80,
    profit: 0.70,
    profit_margin: 14.58,
    buy_volume: 1000000,
    sell_volume: 800000
  },
  {
    item: { name: "Pyerite", type_id: 35 },
    buy_region: { name: "The Forge (Jita)" },
    sell_region: { name: "Sinq Laison (Dodixie)" },
    buy_price: 12.30,
    sell_price: 11.20,
    profit: 1.10,
    profit_margin: 9.82,
    buy_volume: 500000,
    sell_volume: 600000
  }
]

const mockPriceData = [
  { date: '2024-01-01', price: 5.20, volume: 1000000 },
  { date: '2024-01-02', price: 5.35, volume: 1200000 },
  { date: '2024-01-03', price: 5.45, volume: 950000 },
  { date: '2024-01-04', price: 5.30, volume: 1100000 },
  { date: '2024-01-05', price: 5.50, volume: 1300000 },
]

function Dashboard() {
  const [marketHealth, setMarketHealth] = useState({
    active_items: 1250,
    active_regions: 5,
    total_buy_volume: 15000000,
    total_sell_volume: 12000000,
    total_orders: 45000,
    last_update: new Date().toISOString()
  })

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Aktive Items</CardTitle>
            <Package className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{marketHealth.active_items.toLocaleString()}</div>
            <p className="text-xs text-muted-foreground">
              +12% seit letzter Woche
            </p>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Handelsvolumen</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{(marketHealth.total_buy_volume / 1000000).toFixed(1)}M</div>
            <p className="text-xs text-muted-foreground">
              Kauf-Orders heute
            </p>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Aktive Orders</CardTitle>
            <Activity className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{marketHealth.total_orders.toLocaleString()}</div>
            <p className="text-xs text-muted-foreground">
              Alle Regionen
            </p>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Regionen</CardTitle>
            <DollarSign className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{marketHealth.active_regions}</div>
            <p className="text-xs text-muted-foreground">
              Haupthandelsplätze
            </p>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Handelsvolumen Trend</CardTitle>
            <CardDescription>Tägliches Handelsvolumen der letzten 7 Tage</CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={mockPriceData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="volume" stroke="#8884d8" strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Top Arbitrage Möglichkeiten</CardTitle>
            <CardDescription>Profitable Handelsrouten zwischen Regionen</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {mockArbitrageData.map((arb, index) => (
                <div key={index} className="flex items-center justify-between p-3 border rounded-lg">
                  <div>
                    <p className="font-medium">{arb.item.name}</p>
                    <p className="text-sm text-muted-foreground">
                      {arb.sell_region.name} → {arb.buy_region.name}
                    </p>
                  </div>
                  <div className="text-right">
                    <p className="font-bold text-green-600">+{arb.profit.toFixed(2)} ISK</p>
                    <p className="text-sm text-muted-foreground">{arb.profit_margin.toFixed(1)}%</p>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

function ItemBrowser() {
  const [items, setItems] = useState(mockItems)
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedRegion, setSelectedRegion] = useState('')

  const filteredItems = items.filter(item =>
    item.name.toLowerCase().includes(searchTerm.toLowerCase())
  )

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row gap-4">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="Items suchen..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="pl-10"
          />
        </div>
        <Select value={selectedRegion} onValueChange={setSelectedRegion}>
          <SelectTrigger className="w-full sm:w-[200px]">
            <SelectValue placeholder="Region wählen" />
          </SelectTrigger>
          <SelectContent>
            {mockRegions.map(region => (
              <SelectItem key={region.region_id} value={region.region_id.toString()}>
                {region.name}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Items ({filteredItems.length})</CardTitle>
          <CardDescription>Alle verfügbaren Items mit aktuellen Marktdaten</CardDescription>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Name</TableHead>
                <TableHead>Type ID</TableHead>
                <TableHead>Volumen</TableHead>
                <TableHead>Aktueller Preis</TableHead>
                <TableHead>24h Änderung</TableHead>
                <TableHead>Status</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredItems.map(item => (
                <TableRow key={item.type_id}>
                  <TableCell className="font-medium">{item.name}</TableCell>
                  <TableCell>{item.type_id}</TableCell>
                  <TableCell>{item.volume} m³</TableCell>
                  <TableCell>5.45 ISK</TableCell>
                  <TableCell>
                    <div className="flex items-center">
                      <TrendingUp className="h-4 w-4 text-green-500 mr-1" />
                      <span className="text-green-600">+2.3%</span>
                    </div>
                  </TableCell>
                  <TableCell>
                    <Badge variant="outline">Aktiv</Badge>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  )
}

function ArbitrageAnalysis() {
  const [arbitrageData, setArbitrageData] = useState(mockArbitrageData)
  const [minProfit, setMinProfit] = useState(0.5)

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row gap-4">
        <div className="flex-1">
          <label className="text-sm font-medium">Mindestgewinn (ISK)</label>
          <Input
            type="number"
            value={minProfit}
            onChange={(e) => setMinProfit(parseFloat(e.target.value) || 0)}
            step="0.1"
            min="0"
          />
        </div>
        <Button className="sm:mt-6">
          <AlertTriangle className="h-4 w-4 mr-2" />
          Analyse aktualisieren
        </Button>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Arbitrage Möglichkeiten</CardTitle>
          <CardDescription>
            Profitable Handelsrouten zwischen verschiedenen Regionen
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Item</TableHead>
                <TableHead>Kaufen in</TableHead>
                <TableHead>Verkaufen in</TableHead>
                <TableHead>Kaufpreis</TableHead>
                <TableHead>Verkaufspreis</TableHead>
                <TableHead>Gewinn</TableHead>
                <TableHead>Marge</TableHead>
                <TableHead>Volumen</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {arbitrageData.map((arb, index) => (
                <TableRow key={index}>
                  <TableCell className="font-medium">{arb.item.name}</TableCell>
                  <TableCell>{arb.sell_region.name}</TableCell>
                  <TableCell>{arb.buy_region.name}</TableCell>
                  <TableCell>{arb.sell_price.toFixed(2)} ISK</TableCell>
                  <TableCell>{arb.buy_price.toFixed(2)} ISK</TableCell>
                  <TableCell className="text-green-600 font-bold">
                    +{arb.profit.toFixed(2)} ISK
                  </TableCell>
                  <TableCell>{arb.profit_margin.toFixed(1)}%</TableCell>
                  <TableCell>{arb.buy_volume.toLocaleString()}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  )
}

function PriceAnalysis() {
  const [selectedItem, setSelectedItem] = useState('34')
  const [selectedRegion, setSelectedRegion] = useState('10000002')

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row gap-4">
        <Select value={selectedItem} onValueChange={setSelectedItem}>
          <SelectTrigger className="flex-1">
            <SelectValue placeholder="Item wählen" />
          </SelectTrigger>
          <SelectContent>
            {mockItems.map(item => (
              <SelectItem key={item.type_id} value={item.type_id.toString()}>
                {item.name}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
        
        <Select value={selectedRegion} onValueChange={setSelectedRegion}>
          <SelectTrigger className="flex-1">
            <SelectValue placeholder="Region wählen" />
          </SelectTrigger>
          <SelectContent>
            {mockRegions.map(region => (
              <SelectItem key={region.region_id} value={region.region_id.toString()}>
                {region.name}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Preisentwicklung</CardTitle>
            <CardDescription>Historische Preisdaten der letzten 30 Tage</CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={mockPriceData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="price" stroke="#8884d8" strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Handelsvolumen</CardTitle>
            <CardDescription>Tägliches Handelsvolumen</CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={mockPriceData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="volume" fill="#82ca9d" />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Marktstatistiken</CardTitle>
          <CardDescription>Aktuelle Marktdaten für das ausgewählte Item</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="text-center">
              <p className="text-2xl font-bold text-green-600">5.45</p>
              <p className="text-sm text-muted-foreground">Aktueller Preis</p>
            </div>
            <div className="text-center">
              <p className="text-2xl font-bold">5.20 - 5.70</p>
              <p className="text-sm text-muted-foreground">24h Range</p>
            </div>
            <div className="text-center">
              <p className="text-2xl font-bold">1.2M</p>
              <p className="text-sm text-muted-foreground">24h Volumen</p>
            </div>
            <div className="text-center">
              <p className="text-2xl font-bold text-green-600">+2.3%</p>
              <p className="text-sm text-muted-foreground">24h Änderung</p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-background">
        <header className="border-b">
          <div className="container mx-auto px-4 py-4">
            <div className="flex items-center justify-between">
              <h1 className="text-2xl font-bold">EVE Online Trading Tool</h1>
              <nav className="hidden md:flex space-x-6">
                <a href="/" className="text-foreground hover:text-primary">Dashboard</a>
                <a href="/items" className="text-muted-foreground hover:text-primary">Items</a>
                <a href="/arbitrage" className="text-muted-foreground hover:text-primary">Arbitrage</a>
                <a href="/analysis" className="text-muted-foreground hover:text-primary">Analyse</a>
              </nav>
            </div>
          </div>
        </header>

        <main className="container mx-auto px-4 py-8">
          <Tabs defaultValue="dashboard" className="space-y-6">
            <TabsList className="grid w-full grid-cols-4">
              <TabsTrigger value="dashboard">Dashboard</TabsTrigger>
              <TabsTrigger value="items">Items</TabsTrigger>
              <TabsTrigger value="arbitrage">Arbitrage</TabsTrigger>
              <TabsTrigger value="analysis">Analyse</TabsTrigger>
            </TabsList>
            
            <TabsContent value="dashboard">
              <Dashboard />
            </TabsContent>
            
            <TabsContent value="items">
              <ItemBrowser />
            </TabsContent>
            
            <TabsContent value="arbitrage">
              <ArbitrageAnalysis />
            </TabsContent>
            
            <TabsContent value="analysis">
              <PriceAnalysis />
            </TabsContent>
          </Tabs>
        </main>
      </div>
    </Router>
  )
}

export default App

