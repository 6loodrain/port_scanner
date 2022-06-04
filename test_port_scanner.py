from aiohttp.test_utils import AioHTTPTestCase
import unittest
import port_scanner as ps


class MyAppTestCase(AioHTTPTestCase):

    async def get_application(self):
        app = ps.create_app()
        return app

    async def test_good_1(self):
        async with self.client.request("GET", "/scan/140.82.121.4/80/80") as response:
            self.assertEqual(response.status, 200)
            text = await response.text()
        self.assertEqual('[{"port": "80", "state": "open"}]', text)

    async def test_good_2(self):
        async with self.client.request("GET", "/scan/195.19.220.24/1/1000") as response:
            self.assertEqual(response.status, 200)
            text = await response.text()
        self.assertIn('{"port": "443", "state": "open"}', text)

    async def test_out_of_range_start_port(self):
        async with self.client.request("GET", "/scan/140.82.121.4/-1/1000") as response:
            self.assertEqual(response.status, 400)
            text = await response.text()
        self.assertIn('', text)

    async def test_out_of_range_start_port_and_end_port(self):
        async with self.client.request("GET", "/scan/140.82.121.4/5454564/100210") as response:
            self.assertEqual(response.status, 400)
            text = await response.text()
        self.assertIn('', text)

    async def test_out_of_range_end_port(self):
        async with self.client.request("GET", "/scan/140.82.121.4/1/66666") as response:
            self.assertEqual(response.status, 400)
            text = await response.text()
        self.assertIn('', text)

    async def test_start_port_is_bigger_than_end_port(self):
        async with self.client.request("GET", "/scan/140.82.121.4/500/100") as response:
            self.assertEqual(response.status, 400)
            text = await response.text()
        self.assertIn('', text)

    async def test_ip_incorrect_length_5_bytes(self):
        async with self.client.request("GET", "/scan/140.82.121.4.5/1/100") as response:
            self.assertEqual(response.status, 400)
            text = await response.text()
        self.assertIn('', text)

    async def test_ip_incorrect_length_3_bytes(self):
        async with self.client.request("GET", "/scan/140.82.121/1/100") as response:
            self.assertEqual(response.status, 400)
            text = await response.text()
        self.assertIn('', text)

    async def test_ip_1_byte_number(self):
        async with self.client.request("GET", "/scan/1400.82.121.4.5/1/100") as response:
            self.assertEqual(response.status, 400)
            text = await response.text()
        self.assertIn('', text)

    async def test_ip_2_byte_number(self):
        async with self.client.request("GET", "/scan/140.820.121.4.5/1/100") as response:
            self.assertEqual(response.status, 400)
            text = await response.text()
        self.assertIn('', text)

    async def test_ip_3_byte_number(self):
        async with self.client.request("GET", "/scan/140.82.121.400.5/1/100") as response:
            self.assertEqual(response.status, 400)
            text = await response.text()
        self.assertIn('', text)

    async def test_ip_4_byte_number(self):
        async with self.client.request("GET", "/scan/1400.82.121.4.500/1/100") as response:
            self.assertEqual(response.status, 400)
            text = await response.text()
        self.assertIn('', text)

    async def test_ip_more_than_3_params(self):
        async with self.client.request("GET", "/scan/140.82.121.4/1/100/3") as response:
            self.assertEqual(response.status, 404)
            text = await response.text()
        self.assertIn('', text)

    async def test_ip_1_byte_char(self):
        async with self.client.request("GET", "/scan/a.82.121.4.5/1/100") as response:
            self.assertEqual(response.status, 400)
            text = await response.text()
        self.assertIn('', text)

    async def test_ip_2_byte_char(self):
        async with self.client.request("GET", "/scan/140.b.121.4.5/1/100") as response:
            self.assertEqual(response.status, 400)
            text = await response.text()
        self.assertIn('', text)

    async def test_ip_3_byte_char(self):
        async with self.client.request("GET", "/scan/140.82.121.c.5/1/100") as response:
            self.assertEqual(response.status, 400)
            text = await response.text()
        self.assertIn('', text)

    async def test_ip_4_byte_char(self):
        async with self.client.request("GET", "/scan/140.82.121.4.d/1/100") as response:
            self.assertEqual(response.status, 400)
            text = await response.text()
        self.assertIn('', text)

    async def test_ip_separated_str(self):
        async with self.client.request("GET", "/scan/adasd.asdas.sdf.sdf/1/100") as response:
            self.assertEqual(response.status, 400)
            text = await response.text()
        self.assertIn('', text)

    async def test_ip_str(self):
        async with self.client.request("GET", "/scan/kwazzz/1/100") as response:
            self.assertEqual(response.status, 400)
            text = await response.text()
        self.assertIn('', text)

    async def test_ip_less_than_3_params(self):
        async with self.client.request("GET", "/scan/140.82.121.4/1/") as response:
            self.assertEqual(response.status, 404)
            text = await response.text()
        self.assertIn('', text)

    async def test_no_routing(self):
        async with self.client.request("GET", "/") as response:
            self.assertEqual(response.status, 404)
            text = await response.text()
        self.assertIn('', text)

    async def test_bad_routing(self):
        async with self.client.request("GET", "/scam/140.82.121.4/1/80") as response:
            self.assertEqual(response.status, 404)
            text = await response.text()
        self.assertIn('', text)

    async def test_post(self):
        async with self.client.request("POST", "/scan/140.82.121.4/1/80") as response:
            self.assertEqual(response.status, 405)
            text = await response.text()
        self.assertIn('', text)

    async def test_delete(self):
        async with self.client.request("DELETE", "/scan/140.82.121.4/1/80") as response:
            self.assertEqual(response.status, 405)
            text = await response.text()
        self.assertIn('', text)

    async def test_put(self):
        async with self.client.request("PUT", "/scan/140.82.121.4/1/80") as response:
            self.assertEqual(response.status, 405)
            text = await response.text()
        self.assertIn('', text)

    async def test_ip_list(self):
        async with self.client.request("GET", "/scan/[140.82.121.4]/1/80") as response:
            self.assertEqual(response.status, 400)
            text = await response.text()
        self.assertIn('', text)

    async def test_start_port_list(self):
        async with self.client.request("GET", "/scan/140.82.121.4/[1]/80") as response:
            self.assertEqual(response.status, 400)
            text = await response.text()
        self.assertIn('', text)

    async def test_end_port_list(self):
        async with self.client.request("GET", "/scan/140.82.121.4/1/[80]") as response:
            self.assertEqual(response.status, 400)
            text = await response.text()
        self.assertIn('', text)

    async def test_start_port_str(self):
        async with self.client.request("GET", "/scan/140.82.121.4/start/80") as response:
            self.assertEqual(response.status, 400)
            text = await response.text()
        self.assertIn('', text)

    async def test_end_port_str(self):
        async with self.client.request("GET", "/scan/140.82.121.4/1/end") as response:
            self.assertEqual(response.status, 400)
            text = await response.text()
        self.assertIn('', text)


if __name__ == '__main__':
    unittest.main()
