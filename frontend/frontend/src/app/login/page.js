"use client";
import { useState } from "react";
import axios from "axios";
import { API_PATH } from "@/lib/apipath";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import Image from "next/image";
import Link from "next/link";
import { toast } from "sonner";
import { useRouter } from "next/navigation";

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
    // console.log(formData);
    try {
      const formDataEncoded = new URLSearchParams();
      formDataEncoded.append("username", formData.username);
      formDataEncoded.append("password", formData.password);
      const response = await axios.post(API_PATH.AUTH.LOGIN, formDataEncoded, {
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
      });
      // console.log(response)
      if (!response) {
        throw new Error("Login Failed");
      }
      const access_token = response.data.access_token;
      sessionStorage.setItem("token", access_token);
      router.push('/');
      toast.success("Logged in successfully!");
    } catch (err) {
      if (err.response && err.response.data)
        toast.error(
          err.response.data.detail ||
            "Login Failed. Please check your credentials!"
        );
      else {
        toast.error("An unexpected error occured!")
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex justify-center items-center min-h-screen flex-col ">
      <h2 className="text-center font-bold text-3xl mb-3 text-primary">Login</h2>
      <div className="p-4 bg-card shadow-lg rounded-md flex flex-row gap-8">
        <Image
          src="/undraw_authentication_tbfc.svg"
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
            placeholder="Password"
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
            {loading ? "Logging in..." : "Login"}
          </Button>
          <Link href="/signup">
            <Button variant="link" onClick={() => {}} type="button">
              Create account?
            </Button>
          </Link>
        </form>
      </div>
    </div>
  );
}
