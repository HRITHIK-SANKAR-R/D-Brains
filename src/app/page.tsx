import React from "react";
import Link from "next/link";
import Image from "next/image";
import { Button } from "@/components/ui/button";

const pulses = [
  { id: 1, name: "Rice", image: "/placeholder.svg?height=150&width=150" },
  { id: 2, name: "Wheat", image: "/placeholder.svg?height=150&width=150" },
  { id: 3, name: "Onion", image: "/placeholder.svg?height=150&width=150" },
  { id: 4, name: "Brinjal", image: "/placeholder.svg?height=150&width=150" },
  { id: 5, name: "Rajma", image: "/placeholder.svg?height=150&width=150" },
  {
    id: 6,
    name: "Bengal Gram",
    image: "/placeholder.svg?height=150&width=150",
  },
];

export default function HomePage() {
  return (
    <div className="flex flex-col min-h-screen">
      <header className="bg-green-600 text-white p-4">
        <div className="container mx-auto flex justify-between items-center">
          <h1 className="text-2xl font-bold">Smart Farming dApp</h1>
          <nav>
            <Link href="/login" passHref>
              <Button variant="outline" className="mr-2">
                Login
              </Button>
            </Link>
            <Link href="/demo" passHref>
              <Button variant="outline">Show Demo</Button>
            </Link>
          </nav>
        </div>
      </header>

      <main className="flex-grow container mx-auto px-4 py-8">
        <h2 className="text-3xl font-bold text-center mb-8">
          Available Pulses
        </h2>
        <p className="text-center mb-8">
          Connect directly with farmers and purchase fresh pulses with no
          intermediaries!
        </p>
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
          {pulses.map((pulse) => (
            <Link key={pulse.id} href={`/pulse/${pulse.id}`} passHref>
              <div className="bg-white rounded-lg shadow-md overflow-hidden cursor-pointer transition-transform hover:scale-105">
                <Image
                  src={pulse.image}
                  alt={pulse.name}
                  width={150}
                  height={150}
                  layout="responsive"
                />
                <div className="p-4">
                  <h3 className="text-xl font-semibold text-center">
                    {pulse.name}
                  </h3>
                </div>
              </div>
            </Link>
          ))}
        </div>
      </main>

      <footer className="bg-gray-200 py-4">
        <div className="container mx-auto text-center text-sm">
          <p>
            &copy; {new Date().getFullYear()} Smart Farming dApp. All rights
            reserved.
          </p>
        </div>
      </footer>
    </div>
  );
}
