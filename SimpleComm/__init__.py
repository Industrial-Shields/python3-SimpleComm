class SimpleComm:
	SYN = 0x02
	address = 0

	def __init__(self, address = 0):
		SimpleComm.setAddress(address)

	def setAddress(address):
		SimpleComm.address = address

	def getAddress():
		return SimpleComm.address

	async def async_send(stream, packet, destination = None, type = None):
		packet.setSource(SimpleComm.getAddress())

		if destination != None:
			packet.setDestination(destination)

		if type != None:
			packet.setType(type)

		data = packet.getData()
		buffer = bytearray()
		buffer.append(SimpleComm.SYN)
		buffer.append(len(data) + 4)
		buffer.append(packet.getDestination())
		buffer.append(packet.getSource())
		buffer.append(packet.getType())
		buffer += data
		buffer.append(SimpleComm.calcCRC(buffer[2:]))

		if has_aioserial and isinstance(stream, aioserial.Serial):
			await stream.write_async(bytes(buffer))
		else:
			stream.write(bytes(buffer))

	def send(stream, packet, destination = None, type = None):
		packet.setSource(SimpleComm.getAddress())

		if destination != None:
			packet.setDestination(destination)

		if type != None:
			packet.setType(type)

		data = packet.getData()
		buffer = bytearray()
		buffer.append(SimpleComm.SYN)
		buffer.append(len(data) + 4)
		buffer.append(packet.getDestination())
		buffer.append(packet.getSource())
		buffer.append(packet.getType())
		buffer += data
		buffer.append(SimpleComm.calcCRC(buffer[2:]))

		stream.write(bytes(buffer))

	async def async_receive(stream):
		if isinstance(stream, aioserial.Serial):
			stream_read_fun = stream.read_async
		else:
			stream_read_fun = stream.read
		try:
			while True:
				r = await stream_read_fun(1)
				if len(r) == 0:
					break

				if r[0] != SimpleComm.SYN:
					continue

				r = await stream_read_fun(1)
				if len(r) == 0:
					break

				tlen = r[0]
				if tlen < 4:
					continue

				buffer = await stream_read_fun(tlen)
				if len(buffer) != tlen:
					break;

				crc = SimpleComm.calcCRC(buffer[0:-1])
				if crc != buffer[-1]:
					continue

				packet = SimplePacket()
				packet.setDestination(buffer[0])
				packet.setSource(buffer[1])
				packet.setType(buffer[2])
				packet.setData(buffer[3:-1])

				return packet

		except:
			return None

		return None

	def receive(stream):
		try:
			while True:
				r = stream.read(1)
				if len(r) == 0:
					break

				if r[0] != SimpleComm.SYN:
					continue

				r = stream.read(1)
				if len(r) == 0:
					break

				tlen = r[0]
				if tlen < 4:
					continue

				buffer = stream.read(tlen)
				if len(buffer) != tlen:
					break;

				crc = SimpleComm.calcCRC(buffer[0:-1])
				if crc != buffer[-1]:
					continue

				packet = SimplePacket()
				packet.setDestination(buffer[0])
				packet.setSource(buffer[1])
				packet.setType(buffer[2])
				packet.setData(buffer[3:-1])

				return packet

		except:
			return None

		return None

	def calcCRC(buffer):
		return sum(buffer) & 0xff
