"use client";
import { useState } from "react";
import axios from "axios";
import { API_PATH } from "@/lib/apipath";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import Image from "next/image";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { toast } from "sonner";

export default function Login() {
  const router = useRouter();
  const [formData, setFormData] = useState({ username: "", password: "" }); 
  const [loading, setLoading] = useState(false);
  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    console.log(formData);
    try {
      const response = await axios.post(API_PATH.AUTH.LOGIN, formData, {
        headers: { "Content-Type": "application/json" },
      });
        if (!response.ok) {
          throw new Error("Login Failed");
        }
      toast.success("Created Account!", {
        description: "You have been redirected to login",
        className: "text-center text-black-500",
      });
      router.push("/login");
    } catch (err) {
      toast.error("Login Failed", {
        description: err.message || "An error occurred during login",
        action: {
          label: "Retry?",
          onClick: () => handleSubmit(e),
        },
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex justify-center items-center min-h-screen flex-col ">
      <h2 className="text-center font-bold text-3xl mb-3 text-white">
        Sign Up
      </h2>
      <div className="p-4 bg-purple-400 shadow-lg rounded-md flex flex-row gap-8">
        <Image
          src="/undraw_sign-up_qamz.svg"
          width={300}
          height={300}
          alt="image"
          className="hidden sm:block"
        ></Image>

        <form onSubmit={handleSubmit} className="w-96 p-8">
          <Label htmlFor="username" className="text-white">
            Username
          </Label>
          <Input
            type="text"
            placeholder="Username"
            id="username"
            className="mb-7"
            value={formData.username}
            onChange={handleChange}
            name="username"
            required
          ></Input>
          <Label htmlFor="password" className="text-white">
            Password
          </Label>
          <Input
            type="password"
            placeholder="password"
            id="password"
            className="mb-16"
            value={formData.password}
            onChange={handleChange}
            name="password"
            required
          ></Input>
          <Button
            variant="outline"
            type="submit"
            disabled={loading}
            className=""
          >
            {loading ? "Logging in..." : "Signup"}
          </Button>
          <Link href="/login">
            <Button variant="link" onClick={() => {}} type="button">
              Already have account?
            </Button>
          </Link>
        </form>
      </div>
    </div>
  );
}
