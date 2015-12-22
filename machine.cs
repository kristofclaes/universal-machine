using System;
using System.Collections.Generic;
using System.Linq;
using System.IO;
using System.Threading.Tasks;

namespace UniversalMachine {
    public class Program {
        public static void Main(string[] args) {
            var machine = new UniversalMachine();
            machine.Boot(args[0]);
        }
    }

    public class UniversalMachine {
        private uint[] registers;
        private List<List<uint>> arrays;
        private Stack<int> freeIndexes;
        private int executionFinger;
        private const long MaximumValue = 4294967296;

        private void Initialize() {
            registers = new uint[8];
            for (int i=0; i<registers.Length; i++) {
                registers[i] = 0;
            }

            arrays = new List<List<uint>>();
            freeIndexes = new Stack<int>();

            arrays.Add(new List<uint>());
            for (int i=0; i<1000; i++) {
                arrays.Add(new List<uint>());
                freeIndexes.Push(i + 1);
            }

            executionFinger = 0;
        }

        public void Boot(string fileLocation) {
            Initialize();
            ReadFile(fileLocation);

            try {
                while(true) {
                    Cycle();
                }
            }
            catch (HaltException) { }
        }

        private void ReadFile(string fileLocation) {
            using (var filestream = File.Open(fileLocation, FileMode.Open))
            using (var binaryStream = new BinaryReader(filestream)) {
                var values = new List<uint>();
                while (binaryStream.BaseStream.Position != binaryStream.BaseStream.Length) {
                    var ba = binaryStream.ReadBytes(4);
                    Array.Reverse(ba);
                    values.Add(BitConverter.ToUInt32(ba, 0));
                }

                arrays[0] = values;
            }
        }

        private void Cycle() {
            uint data = arrays[0][executionFinger];
            var operationCode = GetOperationCode(data);

            var a = GetAValue(data);
            var b = GetBValue(data);
            var c = GetCValue(data);

            switch (operationCode) {
                case OperationCodes.ConditionalMove:
                    ConditionalMove(a, b, c);
                    break;
                case OperationCodes.ArrayIndex:
                    ArrayIndex(a, b, c);
                    break;
                case OperationCodes.ArrayAmendment:
                    ArrayAmendment(a, b, c);
                    break;
                case OperationCodes.Addition:
                    Addition(a, b, c);
                    break;
                case OperationCodes.Multiplication:
                    Multiplication(a, b, c);
                    break;
                case OperationCodes.Division:
                    Division(a, b, c);
                    break;
                case OperationCodes.NotAnd:
                    NotAnd(a, b, c);
                    break;
                case OperationCodes.Halt:
                    Halt();
                    break;
                case OperationCodes.Allocation:
                    Allocation(a, b, c);
                    break;
                case OperationCodes.Abandonment:
                    Abandonment(a, b, c);
                    break;
                case OperationCodes.Output:
                    Output(a, b, c);
                    break;
                case OperationCodes.Input:
                    Input(a, b, c);
                    break;
                case OperationCodes.LoadProgram:
                    LoadProgram(a, b, c);
                    break;
                case OperationCodes.Orthography:
                    var ortValues = GetOrthographyValues(data);
                    Orthography(ortValues.Item1, ortValues.Item2);
                    break;
            }

            if (operationCode != OperationCodes.LoadProgram) {
                executionFinger++;
            }
        }

        private OperationCodes GetOperationCode(uint data) {
            return (OperationCodes)(data >> 28);
        }

        private int GetAValue(uint data) {
            return (int)((data >> 6) & 0x00000007);
        }

        private int GetBValue(uint data) {
            return (int)((data >> 3) & 0x00000007);
        }

        private int GetCValue(uint data) {
            return (int)(data & 0x00000007);
        }

        private Tuple<int, uint> GetOrthographyValues(uint data) {
            return new Tuple<int, uint>((int)((data & 0x0E000000) >> 25), data & 0x01FFFFFF);
        }

        private void ConditionalMove(int a, int b, int c) {
            if (registers[c] != 0) {
                registers[a] = registers[b];
            }
        }

        private void ArrayIndex(int a, int b, int c) {
            registers[a] = arrays[(int)registers[b]][(int)registers[c]];
        }

        private void ArrayAmendment(int a, int b, int c) {
            arrays[(int)registers[a]][(int)registers[b]] = registers[c];
        }

        private void Addition(int a, int b, int c) {
            registers[a] = (uint)((registers[b] + registers[c]) % MaximumValue);
        }

        private void Multiplication(int a, int b, int c) {
            registers[a] = (uint)((registers[b] * registers[c]) % MaximumValue);
        }

        private void Division(int a, int b, int c) {
            if (registers[c] != 0) {
                registers[a] = Convert.ToUInt32(Math.Floor((decimal)registers[b] / registers[c]));
            }
        }

        private void NotAnd(int a, int b, int c) {
            registers[a] = ~(registers[b] & registers[c]);
        }

        private void Halt() {
            throw new HaltException();
        }

        private void Allocation(int a, int b, int c) {
            var list = new List<uint>();
            for (int i=0; i<(int)registers[c]; i++) {
                list.Add(0);
            }

            if (freeIndexes.Count() > 0) {
                var newIndex = freeIndexes.Pop();
                arrays[newIndex] = list;
                registers[b] = Convert.ToUInt32(newIndex);
            }
            else {
                arrays.Add(list);
                registers[b] = Convert.ToUInt32(arrays.Count() - 1);
            }
        }

        private void Abandonment(int a, int b, int c) {
            var index = (int)registers[c];
            if (index != 0) {
                arrays[index] = null;
                freeIndexes.Push(index);
            }
        }

        private void Output(int a, int b, int c) {
            Console.Write(Convert.ToChar(registers[c]));
        }

        private void Input(int a, int b, int c) {
            registers[c] = Convert.ToUInt32(Console.ReadKey().KeyChar);
        }

        private void LoadProgram(int a, int b, int c) {
            var index = (int)registers[b];
            if (index != 0) {
                arrays[0] = new List<uint>(arrays[index]);
            }

            executionFinger = (int)registers[c];
        }

        private void Orthography(int a, uint value) {
            registers[a] = value;
        }

        private class HaltException : Exception { }
    }

    public enum OperationCodes {
        ConditionalMove = 0,
        ArrayIndex = 1,
        ArrayAmendment = 2,
        Addition = 3,
        Multiplication = 4,
        Division = 5,
        NotAnd = 6,
        Halt = 7,
        Allocation = 8,
        Abandonment = 9,
        Output = 10,
        Input = 11,
        LoadProgram = 12,
        Orthography = 13
    }
}
