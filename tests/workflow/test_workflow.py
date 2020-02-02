# import numpy as np
# import time

# import materia

# # TEST TASKS

# # import dlib,numpy as np,materia,timeit
# # def f1(x):
# #     return -(5 + np.exp(-x))
# #
# # def f2(x):
# #     return x**4*np.exp(-x)
# #
# # class F1(materia.Task):
# #     def __init__(self):
# #         super().__init__()
# #         self.settings['x'] = 0
# #     def run(self):
# #         return self.settings['x'],f1(x=self.settings['x'])
# #
# # class F2(materia.Task):
# #     def __init__(self):
# #         super().__init__()
# #         self.settings['x'] = 0
# #     def run(self):
# #         return self.settings['x'],f2(x=self.settings['x'])
# #
# # class Add(materia.Task):
# #     def run(self, a, b):
# #         x,a = a
# #         x,b = b
# #         return x,a + b
# #
# # class SplineMinimize(materia.handler):
# #     def __init__(self):
# #         self.errors = {}
# #
# #     def check(self, x1, error1, x2, error2, x3, error3, x4, error4, x5, error5):
# #         xs = [x1,x2,x3,x4,x5]
# #         fs = [error1,error2,error3,error4,error5]
# #         x_min,x_max = min(xs),max(xs)
# #         [x0,],_ = dlib.find_min_global(lambda a: scipy.interpolate.CubicSpline(xs,fs)(a),[min(xs),],[max(xs),],100)
# #         delta = (x_max - x_min)/100
# #         z = np.linspace(x0-delta,x0+delta,5)
# #         return dlib.find_min_global(lambda a: scipy.interpolate.CubicSpline(z,f(z))(a),[min(z),],[max(z),],100)[0][0]
# #
# # class Minimize(materia.Handler):
# #     def __init__(self):
# #         self.errors = {}
# #     def _get_next_x(self):
# #         def _proxy(x):
# #             try:
# #                 return self.errors[x]
# #             except KeyError:
# #                 raise ValueError(f'{x}')
# #         try:
# #             dlib.find_min_global(_proxy,[-1],[1],len(self.errors)+1)
# #         except ValueError as e:
# #             return float(str(e))
# #     def handle(self):
# #         return [ModifyX(x=self._get_next_x()),materia.RerunPredecessors(),materia.Rerun()]
# #     def check(self, x, error):
# #         #print(self.errors)
# #         print(x,error,abs(error + 6.585979394638855) > 1e-3)
# #         self.errors[x] = error
# #         return abs(error + 6.585979394638855) > 1e-3
# #
# # class ModifyX(materia.ModifyPredecessorSettings):
# #     def __init__(self, x):
# #         self.x = x
# #     def modify(self, settings):
# #         settings['x'] = self.x
# #
# # def run():
# #     tasks = (F1(),F2(),Add())
# #     tasks[-1].settings['handlers'].append(Minimize())
# #     wf = materia.Workflow(tasks=tasks)
# #     wf.link(tasks[0],tasks[2],pass_result_as='a')
# #     wf.link(tasks[1],tasks[2],pass_result_as='b')
# #     return wf.run()


# class Input(materia.Task):
#     def __init__(self, a, handlers=None, name=None):
#         super().__init__(handlers=handlers, name=name)
#         self.a = a

#     def run(self):
#         return self.a


# class MatMul(materia.Task):
#     def run(self, a, b):
#         return a @ b


# class SlowMatMul(materia.Task):
#     def run(self, a, b):
#         time.sleep(0.5)
#         return a @ b


# class Signal(materia.Task):
#     def run(self):
#         return "Signal triggered successfully."


# class SlowSignal(materia.Task):
#     def run(self):
#         time.sleep(0.5)
#         return "Signal triggered successfully."


# class AddOn(materia.Task):
#     def run(self):
#         return "AddOn triggered successfully."


# class PreMulA(materia.Task):
#     def run(self, a):
#         return np.array([[-1, 0], [0, 1]]) @ a


# class NegativeDetHandler(materia.Handler):
#     def __init__(self, requires_kw=None):
#         self.requires_kw = requires_kw

#     def check(self, result, task):
#         return np.linalg.det(result) < 0

#     def handle(self, result, task):
#         return [materia.InsertTasks(PreMulA(), requires_kw=self.requires_kw)]


# class SuccessHandler(materia.Handler):
#     def check(self, result, task):
#         return result == "Signal triggered successfully."

#     def handle(self, result, task):
#         return [materia.InsertTasks(AddOn())]


# # TESTS


# def test_workflow_signal_complicated_success_handler_one_consumer_thread():
#     t0, t1, t2, t3, t4, t5, t6 = (
#         Signal(handlers=[SuccessHandler()]),
#         Signal(handlers=[SuccessHandler()]),
#         Signal(handlers=[SuccessHandler()]),
#         Signal(handlers=[SuccessHandler()]),
#         Signal(handlers=[SuccessHandler()]),
#         Signal(handlers=[SuccessHandler()]),
#         Signal(handlers=[SuccessHandler()]),
#     )

#     t1.requires(t0)
#     t2.requires(t1)
#     t4.requires(t3)
#     t5.requires(t4)
#     t6.requires(t2, t5)

#     out = materia.Workflow(t0, t1, t2, t3, t4, t5, t6).run(num_consumers=1, thread=True)

#     assert out == {
#         0: "Signal triggered successfully.",
#         3: "Signal triggered successfully.",
#         7: "AddOn triggered successfully.",
#         8: "AddOn triggered successfully.",
#         1: "Signal triggered successfully.",
#         4: "Signal triggered successfully.",
#         9: "AddOn triggered successfully.",
#         10: "AddOn triggered successfully.",
#         2: "Signal triggered successfully.",
#         5: "Signal triggered successfully.",
#         11: "AddOn triggered successfully.",
#         12: "AddOn triggered successfully.",
#         6: "Signal triggered successfully.",
#         13: "AddOn triggered successfully.",
#     }


# def test_workflow_multiply_linear_one_consumer_thread():
#     inp0 = Input(a=np.array([[1, 2], [2, 1]]))
#     inp1 = Input(a=np.array([[-3, 1], [-3, 0.5]]))
#     mm0, mm1, mm2 = MatMul(), MatMul(), MatMul()
#     mm0.requires(a=inp0, b=inp1)
#     mm1.requires(a=inp1, b=inp0)
#     mm2.requires(a=mm0, b=mm1)
#     out = materia.Workflow(inp0, inp1, mm0, mm1, mm2).run(num_consumers=1, thread=True)

#     assert set(out.keys()) == set((0, 1, 2, 3, 4))
#     assert np.allclose(out[0], np.array([[1, 2], [2, 1]]))
#     assert np.allclose(out[1], np.array([[-3, 1], [-3, 0.5]]))
#     assert np.allclose(out[2], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[3], np.array([[-1, -5], [-2, -5.5]]))
#     assert np.allclose(out[4], np.array([[5, 34], [4, 31.25]]))


# def test_workflow_multiply_linear_zero_handler_one_consumer_thread():
#     inp0 = Input(a=np.array([[1, 2], [2, 1]]))
#     inp1 = Input(a=np.array([[-3, 1], [-3, 0.5]]))
#     handler = NegativeDetHandler(requires_kw="a")
#     mm0, mm1, mm2 = (
#         MatMul(handlers=[handler]),
#         MatMul(handlers=[handler]),
#         MatMul(handlers=[handler]),
#     )
#     mm0.requires(a=inp0, b=inp1)
#     mm1.requires(a=inp1, b=inp0)
#     mm2.requires(a=mm0, b=mm1)
#     out = materia.Workflow(inp0, inp1, mm0, mm1, mm2).run(num_consumers=1, thread=True)

#     assert set(out.keys()) == set((0, 1, 2, 3, 4, 5, 6))
#     assert np.allclose(out[0], np.array([[1, 2], [2, 1]]))
#     assert np.allclose(out[1], np.array([[-3, 1], [-3, 0.5]]))
#     assert np.allclose(out[2], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[3], np.array([[-1, -5], [-2, -5.5]]))
#     assert np.allclose(out[4], np.array([[13, 56], [-14, -58.75]]))
#     assert np.allclose(out[5], np.array([[9, -2], [-9, 2.5]]))
#     assert np.allclose(out[6], np.array([[1, 5], [-2, -5.5]]))


# def test_workflow_multiply_complicated_one_consumer_thread():
#     inp0 = Input(a=np.array([[1, 2], [2, 1]]))
#     inp1 = Input(a=np.array([[-3, 1], [-3, 0.5]]))
#     mm0, mm1, mm2, mm3, mm4 = MatMul(), MatMul(), MatMul(), MatMul(), MatMul()
#     mm0.requires(a=inp0, b=inp1)
#     mm1.requires(a=inp1, b=inp0)
#     mm2.requires(a=mm0, b=mm1)
#     mm3.requires(a=mm1, b=mm2)
#     mm4.requires(a=mm3, b=mm0)
#     out = materia.Workflow(inp0, inp1, mm0, mm1, mm2, mm3, mm4).run(
#         num_consumers=1, thread=True
#     )

#     assert set(out.keys()) == set((0, 1, 2, 3, 4, 5, 6))
#     assert np.allclose(out[0], np.array([[1, 2], [2, 1]]))
#     assert np.allclose(out[1], np.array([[-3, 1], [-3, 0.5]]))
#     assert np.allclose(out[2], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[3], np.array([[-1, -5], [-2, -5.5]]))
#     assert np.allclose(out[4], np.array([[5, 34], [4, 31.25]]))
#     assert np.allclose(out[5], np.array([[-25, -190.25], [-32, -239.875]]))
#     assert np.allclose(out[6], np.array([[1937.25, -525.625], [2446.875, -663.6875]]))


# def test_workflow_multiply_complicated_zero_handler_one_consumer_thread():
#     inp0 = Input(a=np.array([[1, 2], [2, 1]]))
#     inp1 = Input(a=np.array([[-3, 1], [-3, 0.5]]))
#     handler = NegativeDetHandler(requires_kw="a")
#     mm0, mm1, mm2, mm3, mm4 = (
#         MatMul(handlers=[handler]),
#         MatMul(handlers=[handler]),
#         MatMul(handlers=[handler]),
#         MatMul(handlers=[handler]),
#         MatMul(handlers=[handler]),
#     )
#     mm0.requires(a=inp0, b=inp1)
#     mm1.requires(a=inp1, b=inp0)
#     mm2.requires(a=mm0, b=mm1)
#     mm3.requires(a=mm1, b=mm2)
#     mm4.requires(a=mm3, b=mm0)
#     out = materia.Workflow(inp0, inp1, mm0, mm1, mm2, mm3, mm4).run(
#         num_consumers=1, thread=True
#     )

#     assert set(out.keys()) == set((0, 1, 2, 3, 4, 5, 6, 7, 8))
#     assert np.allclose(out[0], np.array([[1, 2], [2, 1]]))
#     assert np.allclose(out[1], np.array([[-3, 1], [-3, 0.5]]))
#     assert np.allclose(out[2], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[3], np.array([[-1, -5], [-2, -5.5]]))
#     assert np.allclose(out[4], np.array([[13, 56], [-14, -58.75]]))
#     assert np.allclose(out[5], np.array([[-57, -237.75], [51, 211.125]]))
#     assert np.allclose(out[6], np.array([[1626.75, -480.375], [-1441.125, 425.8125]]))


# def test_workflow_multiply_topheavy_complicated_zero_handler_one_consumer_thread():
#     inp0 = Input(a=np.array([[1, 2], [2, 1]]))
#     inp1 = Input(a=np.array([[-3, 1], [-3, 0.5]]))
#     handler = NegativeDetHandler(requires_kw="a")
#     mm0, mm1, mm2, mm3, mm4, mm5 = (
#         MatMul(handlers=[handler]),
#         MatMul(handlers=[handler]),
#         MatMul(handlers=[handler]),
#         MatMul(handlers=[handler]),
#         MatMul(handlers=[handler]),
#         MatMul(handlers=[handler]),
#     )
#     mm0.requires(a=inp0, b=inp1)
#     mm1.requires(a=inp0, b=mm0)
#     mm2.requires(a=inp0, b=inp1)
#     mm3.requires(a=inp0, b=inp1)
#     mm4.requires(a=inp0, b=inp1)
#     mm5.requires(mm0, mm1, mm2, a=mm3, b=mm4)
#     out = materia.Workflow(inp0, inp1, mm0, mm1, mm2, mm3, mm4, mm5).run(
#         num_consumers=1, thread=True
#     )

#     assert set(out.keys()) == set((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12))
#     assert np.allclose(out[0], np.array([[1, 2], [2, 1]]))
#     assert np.allclose(out[1], np.array([[-3, 1], [-3, 0.5]]))
#     assert np.allclose(out[2], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[3], np.array([[-9, 3], [9, -1.5]]))
#     assert np.allclose(out[4], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[5], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[6], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[7], np.array([[99, -23], [-103.5, 24.25]]))
#     assert np.allclose(out[8], np.array([[9, -2], [-9, 2.5]]))
#     assert np.allclose(out[9], np.array([[9, -2], [-9, 2.5]]))
#     assert np.allclose(out[10], np.array([[9, -2], [-9, 2.5]]))
#     assert np.allclose(out[11], np.array([[9, -2], [-9, 2.5]]))
#     assert np.allclose(out[12], np.array([[9, -3], [9, -1.5]]))


# def test_workflow_signal_complicated_success_handler_two_consumer_threads():
#     t0, t1, t2, t3, t4, t5, t6 = (
#         Signal(handlers=[SuccessHandler()]),
#         Signal(handlers=[SuccessHandler()]),
#         Signal(handlers=[SuccessHandler()]),
#         Signal(handlers=[SuccessHandler()]),
#         Signal(handlers=[SuccessHandler()]),
#         Signal(handlers=[SuccessHandler()]),
#         Signal(handlers=[SuccessHandler()]),
#     )

#     t1.requires(t0)
#     t2.requires(t1)
#     t4.requires(t3)
#     t5.requires(t4)
#     t6.requires(t2, t5)

#     out = materia.Workflow(t0, t1, t2, t3, t4, t5, t6).run(num_consumers=2, thread=True)

#     assert out == {
#         0: "Signal triggered successfully.",
#         3: "Signal triggered successfully.",
#         7: "AddOn triggered successfully.",
#         8: "AddOn triggered successfully.",
#         1: "Signal triggered successfully.",
#         4: "Signal triggered successfully.",
#         9: "AddOn triggered successfully.",
#         10: "AddOn triggered successfully.",
#         2: "Signal triggered successfully.",
#         5: "Signal triggered successfully.",
#         11: "AddOn triggered successfully.",
#         12: "AddOn triggered successfully.",
#         6: "Signal triggered successfully.",
#         13: "AddOn triggered successfully.",
#     }


# def test_workflow_multiply_linear_two_consumer_threads():
#     inp0 = Input(a=np.array([[1, 2], [2, 1]]))
#     inp1 = Input(a=np.array([[-3, 1], [-3, 0.5]]))
#     mm0, mm1, mm2 = MatMul(), MatMul(), MatMul()
#     mm0.requires(a=inp0, b=inp1)
#     mm1.requires(a=inp1, b=inp0)
#     mm2.requires(a=mm0, b=mm1)
#     out = materia.Workflow(inp0, inp1, mm0, mm1, mm2).run(num_consumers=2, thread=True)

#     assert set(out.keys()) == set((0, 1, 2, 3, 4))
#     assert np.allclose(out[0], np.array([[1, 2], [2, 1]]))
#     assert np.allclose(out[1], np.array([[-3, 1], [-3, 0.5]]))
#     assert np.allclose(out[2], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[3], np.array([[-1, -5], [-2, -5.5]]))
#     assert np.allclose(out[4], np.array([[5, 34], [4, 31.25]]))


# def test_workflow_multiply_linear_zero_handler_two_consumer_threads():
#     inp0 = Input(a=np.array([[1, 2], [2, 1]]))
#     inp1 = Input(a=np.array([[-3, 1], [-3, 0.5]]))
#     handler = NegativeDetHandler(requires_kw="a")
#     mm0, mm1, mm2 = (
#         MatMul(handlers=[handler]),
#         MatMul(handlers=[handler]),
#         MatMul(handlers=[handler]),
#     )
#     mm0.requires(a=inp0, b=inp1)
#     mm1.requires(a=inp1, b=inp0)
#     mm2.requires(a=mm0, b=mm1)
#     out = materia.Workflow(inp0, inp1, mm0, mm1, mm2).run(num_consumers=2, thread=True)

#     assert set(out.keys()) == set((0, 1, 2, 3, 4, 5, 6))
#     assert np.allclose(out[0], np.array([[1, 2], [2, 1]]))
#     assert np.allclose(out[1], np.array([[-3, 1], [-3, 0.5]]))
#     assert np.allclose(out[2], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[3], np.array([[-1, -5], [-2, -5.5]]))
#     assert np.allclose(out[4], np.array([[13, 56], [-14, -58.75]]))
#     assert (
#         np.allclose(out[5], np.array([[9, -2], [-9, 2.5]]))
#         and np.allclose(out[6], np.array([[1, 5], [-2, -5.5]]))
#     ) or (
#         np.allclose(out[6], np.array([[9, -2], [-9, 2.5]]))
#         and np.allclose(out[5], np.array([[1, 5], [-2, -5.5]]))
#     )


# def test_workflow_multiply_complicated_two_consumer_threads():
#     inp0 = Input(a=np.array([[1, 2], [2, 1]]))
#     inp1 = Input(a=np.array([[-3, 1], [-3, 0.5]]))
#     mm0, mm1, mm2, mm3, mm4 = MatMul(), MatMul(), MatMul(), MatMul(), MatMul()
#     mm0.requires(a=inp0, b=inp1)
#     mm1.requires(a=inp1, b=inp0)
#     mm2.requires(a=mm0, b=mm1)
#     mm3.requires(a=mm1, b=mm2)
#     mm4.requires(a=mm3, b=mm0)
#     out = materia.Workflow(inp0, inp1, mm0, mm1, mm2, mm3, mm4).run(
#         num_consumers=2, thread=True
#     )

#     assert set(out.keys()) == set((0, 1, 2, 3, 4, 5, 6))
#     assert np.allclose(out[0], np.array([[1, 2], [2, 1]]))
#     assert np.allclose(out[1], np.array([[-3, 1], [-3, 0.5]]))
#     assert np.allclose(out[2], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[3], np.array([[-1, -5], [-2, -5.5]]))
#     assert np.allclose(out[4], np.array([[5, 34], [4, 31.25]]))
#     assert np.allclose(out[5], np.array([[-25, -190.25], [-32, -239.875]]))
#     assert np.allclose(out[6], np.array([[1937.25, -525.625], [2446.875, -663.6875]]))


# def test_workflow_multiply_complicated_zero_handler_two_consumer_threads():
#     inp0 = Input(a=np.array([[1, 2], [2, 1]]))
#     inp1 = Input(a=np.array([[-3, 1], [-3, 0.5]]))
#     handler = NegativeDetHandler(requires_kw="a")
#     mm0, mm1, mm2, mm3, mm4 = (
#         MatMul(handlers=[handler]),
#         MatMul(handlers=[handler]),
#         MatMul(handlers=[handler]),
#         MatMul(handlers=[handler]),
#         MatMul(handlers=[handler]),
#     )
#     mm0.requires(a=inp0, b=inp1)
#     mm1.requires(a=inp1, b=inp0)
#     mm2.requires(a=mm0, b=mm1)
#     mm3.requires(a=mm1, b=mm2)
#     mm4.requires(a=mm3, b=mm0)
#     out = materia.Workflow(inp0, inp1, mm0, mm1, mm2, mm3, mm4).run(
#         num_consumers=2, thread=True
#     )

#     assert set(out.keys()) == set((0, 1, 2, 3, 4, 5, 6, 7, 8))
#     assert np.allclose(out[0], np.array([[1, 2], [2, 1]]))
#     assert np.allclose(out[1], np.array([[-3, 1], [-3, 0.5]]))
#     assert np.allclose(out[2], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[3], np.array([[-1, -5], [-2, -5.5]]))
#     assert np.allclose(out[4], np.array([[13, 56], [-14, -58.75]]))
#     assert np.allclose(out[5], np.array([[-57, -237.75], [51, 211.125]]))
#     assert np.allclose(out[6], np.array([[1626.75, -480.375], [-1441.125, 425.8125]]))


# def test_workflow_multiply_topheavy_complicated_zero_handler_two_consumer_threads():
#     inp0 = Input(a=np.array([[1, 2], [2, 1]]))
#     inp1 = Input(a=np.array([[-3, 1], [-3, 0.5]]))
#     handler = NegativeDetHandler(requires_kw="a")
#     mm0, mm1, mm2, mm3, mm4, mm5 = (
#         MatMul(handlers=[handler]),
#         MatMul(handlers=[handler]),
#         MatMul(handlers=[handler]),
#         MatMul(handlers=[handler]),
#         MatMul(handlers=[handler]),
#         MatMul(handlers=[handler]),
#     )
#     mm0.requires(a=inp0, b=inp1)
#     mm1.requires(a=inp0, b=mm0)
#     mm2.requires(a=inp0, b=inp1)
#     mm3.requires(a=inp0, b=inp1)
#     mm4.requires(a=inp0, b=inp1)
#     mm5.requires(mm0, mm1, mm2, a=mm3, b=mm4)
#     out = materia.Workflow(inp0, inp1, mm0, mm1, mm2, mm3, mm4, mm5).run(
#         num_consumers=2, thread=True
#     )

#     assert set(out.keys()) == set((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12))
#     assert np.allclose(out[0], np.array([[1, 2], [2, 1]]))
#     assert np.allclose(out[1], np.array([[-3, 1], [-3, 0.5]]))
#     assert np.allclose(out[2], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[3], np.array([[-9, 3], [9, -1.5]]))
#     assert np.allclose(out[4], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[5], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[6], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[7], np.array([[99, -23], [-103.5, 24.25]]))
#     assert np.allclose(out[8], np.array([[9, -2], [-9, 2.5]]))
#     assert np.allclose(out[9], np.array([[9, -2], [-9, 2.5]]))
#     assert np.allclose(out[10], np.array([[9, -2], [-9, 2.5]]))
#     assert np.allclose(out[11], np.array([[9, -2], [-9, 2.5]]))
#     assert np.allclose(out[12], np.array([[9, -3], [9, -1.5]]))


# def test_workflow_signal_complicated_success_handler_three_consumer_threads():
#     t0, t1, t2, t3, t4, t5, t6 = (
#         Signal(handlers=[SuccessHandler()]),
#         Signal(handlers=[SuccessHandler()]),
#         Signal(handlers=[SuccessHandler()]),
#         Signal(handlers=[SuccessHandler()]),
#         Signal(handlers=[SuccessHandler()]),
#         Signal(handlers=[SuccessHandler()]),
#         Signal(handlers=[SuccessHandler()]),
#     )

#     t1.requires(t0)
#     t2.requires(t1)
#     t4.requires(t3)
#     t5.requires(t4)
#     t6.requires(t2, t5)

#     out = materia.Workflow(t0, t1, t2, t3, t4, t5, t6).run(num_consumers=3, thread=True)

#     assert out == {
#         0: "Signal triggered successfully.",
#         3: "Signal triggered successfully.",
#         7: "AddOn triggered successfully.",
#         8: "AddOn triggered successfully.",
#         1: "Signal triggered successfully.",
#         4: "Signal triggered successfully.",
#         9: "AddOn triggered successfully.",
#         10: "AddOn triggered successfully.",
#         2: "Signal triggered successfully.",
#         5: "Signal triggered successfully.",
#         11: "AddOn triggered successfully.",
#         12: "AddOn triggered successfully.",
#         6: "Signal triggered successfully.",
#         13: "AddOn triggered successfully.",
#     }


# def test_workflow_multiply_linear_three_consumer_threads():
#     inp0 = Input(a=np.array([[1, 2], [2, 1]]))
#     inp1 = Input(a=np.array([[-3, 1], [-3, 0.5]]))
#     mm0, mm1, mm2 = MatMul(), MatMul(), MatMul()
#     mm0.requires(a=inp0, b=inp1)
#     mm1.requires(a=inp1, b=inp0)
#     mm2.requires(a=mm0, b=mm1)
#     out = materia.Workflow(inp0, inp1, mm0, mm1, mm2).run(num_consumers=3, thread=True)

#     assert set(out.keys()) == set((0, 1, 2, 3, 4))
#     assert np.allclose(out[0], np.array([[1, 2], [2, 1]]))
#     assert np.allclose(out[1], np.array([[-3, 1], [-3, 0.5]]))
#     assert np.allclose(out[2], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[3], np.array([[-1, -5], [-2, -5.5]]))
#     assert np.allclose(out[4], np.array([[5, 34], [4, 31.25]]))


# def test_workflow_multiply_linear_zero_handler_three_consumer_threads():
#     inp0 = Input(a=np.array([[1, 2], [2, 1]]))
#     inp1 = Input(a=np.array([[-3, 1], [-3, 0.5]]))
#     handler = NegativeDetHandler(requires_kw="a")
#     mm0, mm1, mm2 = (
#         MatMul(handlers=[handler]),
#         MatMul(handlers=[handler]),
#         MatMul(handlers=[handler]),
#     )
#     mm0.requires(a=inp0, b=inp1)
#     mm1.requires(a=inp1, b=inp0)
#     mm2.requires(a=mm0, b=mm1)
#     out = materia.Workflow(inp0, inp1, mm0, mm1, mm2).run(num_consumers=3, thread=True)

#     assert set(out.keys()) == set((0, 1, 2, 3, 4, 5, 6))
#     assert np.allclose(out[0], np.array([[1, 2], [2, 1]]))
#     assert np.allclose(out[1], np.array([[-3, 1], [-3, 0.5]]))
#     assert np.allclose(out[2], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[3], np.array([[-1, -5], [-2, -5.5]]))
#     assert np.allclose(out[4], np.array([[13, 56], [-14, -58.75]]))
#     assert (
#         np.allclose(out[5], np.array([[9, -2], [-9, 2.5]]))
#         and np.allclose(out[6], np.array([[1, 5], [-2, -5.5]]))
#     ) or (
#         np.allclose(out[6], np.array([[9, -2], [-9, 2.5]]))
#         and np.allclose(out[5], np.array([[1, 5], [-2, -5.5]]))
#     )


# def test_workflow_multiply_complicated_three_consumer_threads():
#     inp0 = Input(a=np.array([[1, 2], [2, 1]]))
#     inp1 = Input(a=np.array([[-3, 1], [-3, 0.5]]))
#     mm0, mm1, mm2, mm3, mm4 = MatMul(), MatMul(), MatMul(), MatMul(), MatMul()
#     mm0.requires(a=inp0, b=inp1)
#     mm1.requires(a=inp1, b=inp0)
#     mm2.requires(a=mm0, b=mm1)
#     mm3.requires(a=mm1, b=mm2)
#     mm4.requires(a=mm3, b=mm0)
#     out = materia.Workflow(inp0, inp1, mm0, mm1, mm2, mm3, mm4).run(
#         num_consumers=3, thread=True
#     )

#     assert set(out.keys()) == set((0, 1, 2, 3, 4, 5, 6))
#     assert np.allclose(out[0], np.array([[1, 2], [2, 1]]))
#     assert np.allclose(out[1], np.array([[-3, 1], [-3, 0.5]]))
#     assert np.allclose(out[2], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[3], np.array([[-1, -5], [-2, -5.5]]))
#     assert np.allclose(out[4], np.array([[5, 34], [4, 31.25]]))
#     assert np.allclose(out[5], np.array([[-25, -190.25], [-32, -239.875]]))
#     assert np.allclose(out[6], np.array([[1937.25, -525.625], [2446.875, -663.6875]]))


# def test_workflow_multiply_complicated_zero_handler_three_consumer_threads():
#     inp0 = Input(a=np.array([[1, 2], [2, 1]]))
#     inp1 = Input(a=np.array([[-3, 1], [-3, 0.5]]))
#     handler = NegativeDetHandler(requires_kw="a")
#     mm0, mm1, mm2, mm3, mm4 = (
#         MatMul(handlers=[handler]),
#         MatMul(handlers=[handler]),
#         MatMul(handlers=[handler]),
#         MatMul(handlers=[handler]),
#         MatMul(handlers=[handler]),
#     )
#     mm0.requires(a=inp0, b=inp1)
#     mm1.requires(a=inp1, b=inp0)
#     mm2.requires(a=mm0, b=mm1)
#     mm3.requires(a=mm1, b=mm2)
#     mm4.requires(a=mm3, b=mm0)
#     out = materia.Workflow(inp0, inp1, mm0, mm1, mm2, mm3, mm4).run(
#         num_consumers=3, thread=True
#     )

#     assert set(out.keys()) == set((0, 1, 2, 3, 4, 5, 6, 7, 8))
#     assert np.allclose(out[0], np.array([[1, 2], [2, 1]]))
#     assert np.allclose(out[1], np.array([[-3, 1], [-3, 0.5]]))
#     assert np.allclose(out[2], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[3], np.array([[-1, -5], [-2, -5.5]]))
#     assert np.allclose(out[4], np.array([[13, 56], [-14, -58.75]]))
#     assert np.allclose(out[5], np.array([[-57, -237.75], [51, 211.125]]))
#     assert np.allclose(out[6], np.array([[1626.75, -480.375], [-1441.125, 425.8125]]))


# def test_workflow_multiply_topheavy_complicated_zero_handler_three_consumer_threads():
#     inp0 = Input(a=np.array([[1, 2], [2, 1]]))
#     inp1 = Input(a=np.array([[-3, 1], [-3, 0.5]]))
#     handler = NegativeDetHandler(requires_kw="a")
#     mm0, mm1, mm2, mm3, mm4, mm5 = (
#         MatMul(handlers=[handler]),
#         MatMul(handlers=[handler]),
#         MatMul(handlers=[handler]),
#         MatMul(handlers=[handler]),
#         MatMul(handlers=[handler]),
#         MatMul(handlers=[handler]),
#     )
#     mm0.requires(a=inp0, b=inp1)
#     mm1.requires(a=inp0, b=mm0)
#     mm2.requires(a=inp0, b=inp1)
#     mm3.requires(a=inp0, b=inp1)
#     mm4.requires(a=inp0, b=inp1)
#     mm5.requires(mm0, mm1, mm2, a=mm3, b=mm4)
#     out = materia.Workflow(inp0, inp1, mm0, mm1, mm2, mm3, mm4, mm5).run(
#         num_consumers=3, thread=True
#     )

#     assert set(out.keys()) == set((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12))
#     assert np.allclose(out[0], np.array([[1, 2], [2, 1]]))
#     assert np.allclose(out[1], np.array([[-3, 1], [-3, 0.5]]))
#     assert np.allclose(out[2], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[3], np.array([[-9, 3], [9, -1.5]]))
#     assert np.allclose(out[4], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[5], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[6], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[7], np.array([[99, -23], [-103.5, 24.25]]))
#     assert np.allclose(out[8], np.array([[9, -2], [-9, 2.5]]))
#     assert np.allclose(out[9], np.array([[9, -2], [-9, 2.5]]))
#     assert np.allclose(out[10], np.array([[9, -2], [-9, 2.5]]))
#     assert np.allclose(out[11], np.array([[9, -2], [-9, 2.5]]))
#     assert np.allclose(out[12], np.array([[9, -3], [9, -1.5]]))


# def test_workflow_signal_complicated_success_handler_one_consumer_process():
#     t0, t1, t2, t3, t4, t5, t6 = (
#         Signal(handlers=[SuccessHandler()], name="t0"),
#         Signal(handlers=[SuccessHandler()], name="t1"),
#         Signal(handlers=[SuccessHandler()], name="t2"),
#         Signal(handlers=[SuccessHandler()], name="t3"),
#         Signal(handlers=[SuccessHandler()], name="t4"),
#         Signal(handlers=[SuccessHandler()], name="t5"),
#         Signal(handlers=[SuccessHandler()], name="t6"),
#     )

#     t1.requires(t0)
#     t2.requires(t1)
#     t4.requires(t3)
#     t5.requires(t4)
#     t6.requires(t2, t5)

#     out = materia.Workflow(t0, t1, t2, t3, t4, t5, t6).run(num_consumers=1, thread=False)

#     assert out == {
#         0: "Signal triggered successfully.",
#         3: "Signal triggered successfully.",
#         7: "AddOn triggered successfully.",
#         8: "AddOn triggered successfully.",
#         1: "Signal triggered successfully.",
#         4: "Signal triggered successfully.",
#         9: "AddOn triggered successfully.",
#         10: "AddOn triggered successfully.",
#         2: "Signal triggered successfully.",
#         5: "Signal triggered successfully.",
#         11: "AddOn triggered successfully.",
#         12: "AddOn triggered successfully.",
#         6: "Signal triggered successfully.",
#         13: "AddOn triggered successfully.",
#     }


# def test_workflow_multiply_linear_one_consumer_process():
#     inp0 = Input(a=np.array([[1, 2], [2, 1]]))
#     inp1 = Input(a=np.array([[-3, 1], [-3, 0.5]]))
#     mm0, mm1, mm2 = MatMul(), MatMul(), MatMul()
#     mm0.requires(a=inp0, b=inp1)
#     mm1.requires(a=inp1, b=inp0)
#     mm2.requires(a=mm0, b=mm1)
#     out = materia.Workflow(inp0, inp1, mm0, mm1, mm2).run(num_consumers=1, thread=False)

#     assert set(out.keys()) == set((0, 1, 2, 3, 4))
#     assert np.allclose(out[0], np.array([[1, 2], [2, 1]]))
#     assert np.allclose(out[1], np.array([[-3, 1], [-3, 0.5]]))
#     assert np.allclose(out[2], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[3], np.array([[-1, -5], [-2, -5.5]]))
#     assert np.allclose(out[4], np.array([[5, 34], [4, 31.25]]))


# def test_workflow_multiply_linear_zero_handler_one_consumer_process():
#     inp0 = Input(a=np.array([[1, 2], [2, 1]]))
#     inp1 = Input(a=np.array([[-3, 1], [-3, 0.5]]))
#     handler = NegativeDetHandler(requires_kw="a")
#     mm0, mm1, mm2 = (
#         MatMul(handlers=[handler]),
#         MatMul(handlers=[handler]),
#         MatMul(handlers=[handler]),
#     )
#     mm0.requires(a=inp0, b=inp1)
#     mm1.requires(a=inp1, b=inp0)
#     mm2.requires(a=mm0, b=mm1)
#     out = materia.Workflow(inp0, inp1, mm0, mm1, mm2).run(num_consumers=1, thread=False)

#     assert set(out.keys()) == set((0, 1, 2, 3, 4, 5, 6))
#     assert np.allclose(out[0], np.array([[1, 2], [2, 1]]))
#     assert np.allclose(out[1], np.array([[-3, 1], [-3, 0.5]]))
#     assert np.allclose(out[2], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[3], np.array([[-1, -5], [-2, -5.5]]))
#     assert np.allclose(out[4], np.array([[13, 56], [-14, -58.75]]))
#     assert np.allclose(out[5], np.array([[9, -2], [-9, 2.5]]))
#     assert np.allclose(out[6], np.array([[1, 5], [-2, -5.5]]))


# def test_workflow_multiply_complicated_one_consumer_process():
#     inp0 = Input(a=np.array([[1, 2], [2, 1]]))
#     inp1 = Input(a=np.array([[-3, 1], [-3, 0.5]]))
#     mm0, mm1, mm2, mm3, mm4 = MatMul(), MatMul(), MatMul(), MatMul(), MatMul()
#     mm0.requires(a=inp0, b=inp1)
#     mm1.requires(a=inp1, b=inp0)
#     mm2.requires(a=mm0, b=mm1)
#     mm3.requires(a=mm1, b=mm2)
#     mm4.requires(a=mm3, b=mm0)
#     out = materia.Workflow(inp0, inp1, mm0, mm1, mm2, mm3, mm4).run(
#         num_consumers=1, thread=False
#     )

#     assert set(out.keys()) == set((0, 1, 2, 3, 4, 5, 6))
#     assert np.allclose(out[0], np.array([[1, 2], [2, 1]]))
#     assert np.allclose(out[1], np.array([[-3, 1], [-3, 0.5]]))
#     assert np.allclose(out[2], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[3], np.array([[-1, -5], [-2, -5.5]]))
#     assert np.allclose(out[4], np.array([[5, 34], [4, 31.25]]))
#     assert np.allclose(out[5], np.array([[-25, -190.25], [-32, -239.875]]))
#     assert np.allclose(out[6], np.array([[1937.25, -525.625], [2446.875, -663.6875]]))


# def test_workflow_multiply_complicated_zero_handler_one_consumer_process():
#     inp0 = Input(a=np.array([[1, 2], [2, 1]]))
#     inp1 = Input(a=np.array([[-3, 1], [-3, 0.5]]))
#     handler = NegativeDetHandler(requires_kw="a")
#     mm0, mm1, mm2, mm3, mm4 = (
#         MatMul(handlers=[handler]),
#         MatMul(handlers=[handler]),
#         MatMul(handlers=[handler]),
#         MatMul(handlers=[handler]),
#         MatMul(handlers=[handler]),
#     )
#     mm0.requires(a=inp0, b=inp1)
#     mm1.requires(a=inp1, b=inp0)
#     mm2.requires(a=mm0, b=mm1)
#     mm3.requires(a=mm1, b=mm2)
#     mm4.requires(a=mm3, b=mm0)
#     out = materia.Workflow(inp0, inp1, mm0, mm1, mm2, mm3, mm4).run(
#         num_consumers=1, thread=False
#     )

#     assert set(out.keys()) == set((0, 1, 2, 3, 4, 5, 6, 7, 8))
#     assert np.allclose(out[0], np.array([[1, 2], [2, 1]]))
#     assert np.allclose(out[1], np.array([[-3, 1], [-3, 0.5]]))
#     assert np.allclose(out[2], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[3], np.array([[-1, -5], [-2, -5.5]]))
#     assert np.allclose(out[4], np.array([[13, 56], [-14, -58.75]]))
#     assert np.allclose(out[5], np.array([[-57, -237.75], [51, 211.125]]))
#     assert np.allclose(out[6], np.array([[1626.75, -480.375], [-1441.125, 425.8125]]))


# def test_workflow_multiply_topheavy_complicated_zero_handler_one_consumer_process():
#     inp0 = Input(a=np.array([[1, 2], [2, 1]]))
#     inp1 = Input(a=np.array([[-3, 1], [-3, 0.5]]))
#     handler = NegativeDetHandler(requires_kw="a")
#     mm0, mm1, mm2, mm3, mm4, mm5 = (
#         MatMul(handlers=[handler]),
#         MatMul(handlers=[handler]),
#         MatMul(handlers=[handler]),
#         MatMul(handlers=[handler]),
#         MatMul(handlers=[handler]),
#         MatMul(handlers=[handler]),
#     )
#     mm0.requires(a=inp0, b=inp1)
#     mm1.requires(a=inp0, b=mm0)
#     mm2.requires(a=inp0, b=inp1)
#     mm3.requires(a=inp0, b=inp1)
#     mm4.requires(a=inp0, b=inp1)
#     mm5.requires(mm0, mm1, mm2, a=mm3, b=mm4)
#     out = materia.Workflow(inp0, inp1, mm0, mm1, mm2, mm3, mm4, mm5).run(
#         num_consumers=1, thread=False
#     )

#     assert set(out.keys()) == set((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12))
#     assert np.allclose(out[0], np.array([[1, 2], [2, 1]]))
#     assert np.allclose(out[1], np.array([[-3, 1], [-3, 0.5]]))
#     assert np.allclose(out[2], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[3], np.array([[-9, 3], [9, -1.5]]))
#     assert np.allclose(out[4], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[5], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[6], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[7], np.array([[99, -23], [-103.5, 24.25]]))
#     assert np.allclose(out[8], np.array([[9, -2], [-9, 2.5]]))
#     assert np.allclose(out[9], np.array([[9, -2], [-9, 2.5]]))
#     assert np.allclose(out[10], np.array([[9, -2], [-9, 2.5]]))
#     assert np.allclose(out[11], np.array([[9, -2], [-9, 2.5]]))
#     assert np.allclose(out[12], np.array([[9, -3], [9, -1.5]]))


# def test_workflow_signal_complicated_success_handler_two_consumer_processes():
#     t0, t1, t2, t3, t4, t5, t6 = (
#         Signal(handlers=[SuccessHandler()]),
#         Signal(handlers=[SuccessHandler()]),
#         Signal(handlers=[SuccessHandler()]),
#         Signal(handlers=[SuccessHandler()]),
#         Signal(handlers=[SuccessHandler()]),
#         Signal(handlers=[SuccessHandler()]),
#         Signal(handlers=[SuccessHandler()]),
#     )

#     t1.requires(t0)
#     t2.requires(t1)
#     t4.requires(t3)
#     t5.requires(t4)
#     t6.requires(t2, t5)

#     out = materia.Workflow(t0, t1, t2, t3, t4, t5, t6).run(num_consumers=2, thread=False)

#     assert out == {
#         0: "Signal triggered successfully.",
#         3: "Signal triggered successfully.",
#         7: "AddOn triggered successfully.",
#         8: "AddOn triggered successfully.",
#         1: "Signal triggered successfully.",
#         4: "Signal triggered successfully.",
#         9: "AddOn triggered successfully.",
#         10: "AddOn triggered successfully.",
#         2: "Signal triggered successfully.",
#         5: "Signal triggered successfully.",
#         11: "AddOn triggered successfully.",
#         12: "AddOn triggered successfully.",
#         6: "Signal triggered successfully.",
#         13: "AddOn triggered successfully.",
#     }


# def test_workflow_multiply_linear_two_consumer_processes():
#     inp0 = Input(a=np.array([[1, 2], [2, 1]]))
#     inp1 = Input(a=np.array([[-3, 1], [-3, 0.5]]))
#     mm0, mm1, mm2 = MatMul(), MatMul(), MatMul()
#     mm0.requires(a=inp0, b=inp1)
#     mm1.requires(a=inp1, b=inp0)
#     mm2.requires(a=mm0, b=mm1)
#     out = materia.Workflow(inp0, inp1, mm0, mm1, mm2).run(num_consumers=2, thread=False)

#     assert set(out.keys()) == set((0, 1, 2, 3, 4))
#     assert np.allclose(out[0], np.array([[1, 2], [2, 1]]))
#     assert np.allclose(out[1], np.array([[-3, 1], [-3, 0.5]]))
#     assert np.allclose(out[2], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[3], np.array([[-1, -5], [-2, -5.5]]))
#     assert np.allclose(out[4], np.array([[5, 34], [4, 31.25]]))


# def test_workflow_multiply_linear_zero_handler_two_consumer_processes():
#     inp0 = Input(a=np.array([[1, 2], [2, 1]]))
#     inp1 = Input(a=np.array([[-3, 1], [-3, 0.5]]))
#     handler = NegativeDetHandler(requires_kw="a")
#     mm0, mm1, mm2 = (
#         MatMul(handlers=[handler]),
#         MatMul(handlers=[handler]),
#         MatMul(handlers=[handler]),
#     )
#     mm0.requires(a=inp0, b=inp1)
#     mm1.requires(a=inp1, b=inp0)
#     mm2.requires(a=mm0, b=mm1)
#     out = materia.Workflow(inp0, inp1, mm0, mm1, mm2).run(num_consumers=2, thread=False)

#     assert set(out.keys()) == set((0, 1, 2, 3, 4, 5, 6))
#     assert np.allclose(out[0], np.array([[1, 2], [2, 1]]))
#     assert np.allclose(out[1], np.array([[-3, 1], [-3, 0.5]]))
#     assert np.allclose(out[2], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[3], np.array([[-1, -5], [-2, -5.5]]))
#     assert np.allclose(out[4], np.array([[13, 56], [-14, -58.75]]))
#     assert (
#         np.allclose(out[5], np.array([[9, -2], [-9, 2.5]]))
#         and np.allclose(out[6], np.array([[1, 5], [-2, -5.5]]))
#     ) or (
#         np.allclose(out[6], np.array([[9, -2], [-9, 2.5]]))
#         and np.allclose(out[5], np.array([[1, 5], [-2, -5.5]]))
#     )


# def test_workflow_multiply_complicated_two_consumer_processes():
#     inp0 = Input(a=np.array([[1, 2], [2, 1]]))
#     inp1 = Input(a=np.array([[-3, 1], [-3, 0.5]]))
#     mm0, mm1, mm2, mm3, mm4 = MatMul(), MatMul(), MatMul(), MatMul(), MatMul()
#     mm0.requires(a=inp0, b=inp1)
#     mm1.requires(a=inp1, b=inp0)
#     mm2.requires(a=mm0, b=mm1)
#     mm3.requires(a=mm1, b=mm2)
#     mm4.requires(a=mm3, b=mm0)
#     out = materia.Workflow(inp0, inp1, mm0, mm1, mm2, mm3, mm4).run(
#         num_consumers=2, thread=False
#     )

#     assert set(out.keys()) == set((0, 1, 2, 3, 4, 5, 6))
#     assert np.allclose(out[0], np.array([[1, 2], [2, 1]]))
#     assert np.allclose(out[1], np.array([[-3, 1], [-3, 0.5]]))
#     assert np.allclose(out[2], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[3], np.array([[-1, -5], [-2, -5.5]]))
#     assert np.allclose(out[4], np.array([[5, 34], [4, 31.25]]))
#     assert np.allclose(out[5], np.array([[-25, -190.25], [-32, -239.875]]))
#     assert np.allclose(out[6], np.array([[1937.25, -525.625], [2446.875, -663.6875]]))


# def test_workflow_multiply_complicated_zero_handler_two_consumer_processes():
#     inp0 = Input(a=np.array([[1, 2], [2, 1]]))
#     inp1 = Input(a=np.array([[-3, 1], [-3, 0.5]]))
#     handler = NegativeDetHandler(requires_kw="a")
#     mm0, mm1, mm2, mm3, mm4 = (
#         MatMul(handlers=[handler]),
#         MatMul(handlers=[handler]),
#         MatMul(handlers=[handler]),
#         MatMul(handlers=[handler]),
#         MatMul(handlers=[handler]),
#     )
#     mm0.requires(a=inp0, b=inp1)
#     mm1.requires(a=inp1, b=inp0)
#     mm2.requires(a=mm0, b=mm1)
#     mm3.requires(a=mm1, b=mm2)
#     mm4.requires(a=mm3, b=mm0)
#     out = materia.Workflow(inp0, inp1, mm0, mm1, mm2, mm3, mm4).run(
#         num_consumers=2, thread=False
#     )

#     assert set(out.keys()) == set((0, 1, 2, 3, 4, 5, 6, 7, 8))
#     assert np.allclose(out[0], np.array([[1, 2], [2, 1]]))
#     assert np.allclose(out[1], np.array([[-3, 1], [-3, 0.5]]))
#     assert np.allclose(out[2], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[3], np.array([[-1, -5], [-2, -5.5]]))
#     assert np.allclose(out[4], np.array([[13, 56], [-14, -58.75]]))
#     assert np.allclose(out[5], np.array([[-57, -237.75], [51, 211.125]]))
#     assert np.allclose(out[6], np.array([[1626.75, -480.375], [-1441.125, 425.8125]]))


# def test_workflow_multiply_topheavy_complicated_zero_handler_two_consumer_processes():
#     inp0 = Input(a=np.array([[1, 2], [2, 1]]))
#     inp1 = Input(a=np.array([[-3, 1], [-3, 0.5]]))
#     handler = NegativeDetHandler(requires_kw="a")
#     mm0, mm1, mm2, mm3, mm4, mm5 = (
#         MatMul(handlers=[handler]),
#         MatMul(handlers=[handler]),
#         MatMul(handlers=[handler]),
#         MatMul(handlers=[handler]),
#         MatMul(handlers=[handler]),
#         MatMul(handlers=[handler]),
#     )
#     mm0.requires(a=inp0, b=inp1)
#     mm1.requires(a=inp0, b=mm0)
#     mm2.requires(a=inp0, b=inp1)
#     mm3.requires(a=inp0, b=inp1)
#     mm4.requires(a=inp0, b=inp1)
#     mm5.requires(mm0, mm1, mm2, a=mm3, b=mm4)
#     out = materia.Workflow(inp0, inp1, mm0, mm1, mm2, mm3, mm4, mm5).run(
#         num_consumers=2, thread=False
#     )

#     assert set(out.keys()) == set((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12))
#     assert np.allclose(out[0], np.array([[1, 2], [2, 1]]))
#     assert np.allclose(out[1], np.array([[-3, 1], [-3, 0.5]]))
#     assert np.allclose(out[2], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[3], np.array([[-9, 3], [9, -1.5]]))
#     assert np.allclose(out[4], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[5], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[6], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[7], np.array([[99, -23], [-103.5, 24.25]]))
#     assert np.allclose(out[8], np.array([[9, -2], [-9, 2.5]]))
#     assert np.allclose(out[9], np.array([[9, -2], [-9, 2.5]]))
#     assert np.allclose(out[10], np.array([[9, -2], [-9, 2.5]]))
#     assert np.allclose(out[11], np.array([[9, -2], [-9, 2.5]]))
#     assert np.allclose(out[12], np.array([[9, -3], [9, -1.5]]))


# def test_workflow_signal_complicated_success_handler_three_consumer_processes():
#     t0, t1, t2, t3, t4, t5, t6 = (
#         Signal(handlers=[SuccessHandler()]),
#         Signal(handlers=[SuccessHandler()]),
#         Signal(handlers=[SuccessHandler()]),
#         Signal(handlers=[SuccessHandler()]),
#         Signal(handlers=[SuccessHandler()]),
#         Signal(handlers=[SuccessHandler()]),
#         Signal(handlers=[SuccessHandler()]),
#     )

#     t1.requires(t0)
#     t2.requires(t1)
#     t4.requires(t3)
#     t5.requires(t4)
#     t6.requires(t2, t5)

#     out = materia.Workflow(t0, t1, t2, t3, t4, t5, t6).run(num_consumers=3, thread=False)

#     assert out == {
#         0: "Signal triggered successfully.",
#         3: "Signal triggered successfully.",
#         7: "AddOn triggered successfully.",
#         8: "AddOn triggered successfully.",
#         1: "Signal triggered successfully.",
#         4: "Signal triggered successfully.",
#         9: "AddOn triggered successfully.",
#         10: "AddOn triggered successfully.",
#         2: "Signal triggered successfully.",
#         5: "Signal triggered successfully.",
#         11: "AddOn triggered successfully.",
#         12: "AddOn triggered successfully.",
#         6: "Signal triggered successfully.",
#         13: "AddOn triggered successfully.",
#     }


# def test_workflow_multiply_linear_three_consumer_processes():
#     inp0 = Input(a=np.array([[1, 2], [2, 1]]))
#     inp1 = Input(a=np.array([[-3, 1], [-3, 0.5]]))
#     mm0, mm1, mm2 = MatMul(), MatMul(), MatMul()
#     mm0.requires(a=inp0, b=inp1)
#     mm1.requires(a=inp1, b=inp0)
#     mm2.requires(a=mm0, b=mm1)
#     out = materia.Workflow(inp0, inp1, mm0, mm1, mm2).run(num_consumers=3, thread=False)

#     assert set(out.keys()) == set((0, 1, 2, 3, 4))
#     assert np.allclose(out[0], np.array([[1, 2], [2, 1]]))
#     assert np.allclose(out[1], np.array([[-3, 1], [-3, 0.5]]))
#     assert np.allclose(out[2], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[3], np.array([[-1, -5], [-2, -5.5]]))
#     assert np.allclose(out[4], np.array([[5, 34], [4, 31.25]]))


# def test_workflow_multiply_linear_zero_handler_three_consumer_processes():
#     inp0 = Input(a=np.array([[1, 2], [2, 1]]))
#     inp1 = Input(a=np.array([[-3, 1], [-3, 0.5]]))
#     handler = NegativeDetHandler(requires_kw="a")
#     mm0, mm1, mm2 = (
#         MatMul(handlers=[handler]),
#         MatMul(handlers=[handler]),
#         MatMul(handlers=[handler]),
#     )
#     mm0.requires(a=inp0, b=inp1)
#     mm1.requires(a=inp1, b=inp0)
#     mm2.requires(a=mm0, b=mm1)
#     out = materia.Workflow(inp0, inp1, mm0, mm1, mm2).run(num_consumers=3, thread=False)

#     assert set(out.keys()) == set((0, 1, 2, 3, 4, 5, 6))
#     assert np.allclose(out[0], np.array([[1, 2], [2, 1]]))
#     assert np.allclose(out[1], np.array([[-3, 1], [-3, 0.5]]))
#     assert np.allclose(out[2], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[3], np.array([[-1, -5], [-2, -5.5]]))
#     assert np.allclose(out[4], np.array([[13, 56], [-14, -58.75]]))
#     assert (
#         np.allclose(out[5], np.array([[9, -2], [-9, 2.5]]))
#         and np.allclose(out[6], np.array([[1, 5], [-2, -5.5]]))
#     ) or (
#         np.allclose(out[6], np.array([[9, -2], [-9, 2.5]]))
#         and np.allclose(out[5], np.array([[1, 5], [-2, -5.5]]))
#     )


# def test_workflow_multiply_complicated_three_consumer_processes():
#     inp0 = Input(a=np.array([[1, 2], [2, 1]]))
#     inp1 = Input(a=np.array([[-3, 1], [-3, 0.5]]))
#     mm0, mm1, mm2, mm3, mm4 = MatMul(), MatMul(), MatMul(), MatMul(), MatMul()
#     mm0.requires(a=inp0, b=inp1)
#     mm1.requires(a=inp1, b=inp0)
#     mm2.requires(a=mm0, b=mm1)
#     mm3.requires(a=mm1, b=mm2)
#     mm4.requires(a=mm3, b=mm0)
#     out = materia.Workflow(inp0, inp1, mm0, mm1, mm2, mm3, mm4).run(
#         num_consumers=3, thread=False
#     )

#     assert set(out.keys()) == set((0, 1, 2, 3, 4, 5, 6))
#     assert np.allclose(out[0], np.array([[1, 2], [2, 1]]))
#     assert np.allclose(out[1], np.array([[-3, 1], [-3, 0.5]]))
#     assert np.allclose(out[2], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[3], np.array([[-1, -5], [-2, -5.5]]))
#     assert np.allclose(out[4], np.array([[5, 34], [4, 31.25]]))
#     assert np.allclose(out[5], np.array([[-25, -190.25], [-32, -239.875]]))
#     assert np.allclose(out[6], np.array([[1937.25, -525.625], [2446.875, -663.6875]]))


# def test_workflow_multiply_complicated_zero_handler_three_consumer_processes():
#     inp0 = Input(a=np.array([[1, 2], [2, 1]]))
#     inp1 = Input(a=np.array([[-3, 1], [-3, 0.5]]))
#     handler = NegativeDetHandler(requires_kw="a")
#     mm0, mm1, mm2, mm3, mm4 = (
#         MatMul(handlers=[handler]),
#         MatMul(handlers=[handler]),
#         MatMul(handlers=[handler]),
#         MatMul(handlers=[handler]),
#         MatMul(handlers=[handler]),
#     )
#     mm0.requires(a=inp0, b=inp1)
#     mm1.requires(a=inp1, b=inp0)
#     mm2.requires(a=mm0, b=mm1)
#     mm3.requires(a=mm1, b=mm2)
#     mm4.requires(a=mm3, b=mm0)
#     out = materia.Workflow(inp0, inp1, mm0, mm1, mm2, mm3, mm4).run(
#         num_consumers=3, thread=False
#     )

#     assert set(out.keys()) == set((0, 1, 2, 3, 4, 5, 6, 7, 8))
#     assert np.allclose(out[0], np.array([[1, 2], [2, 1]]))
#     assert np.allclose(out[1], np.array([[-3, 1], [-3, 0.5]]))
#     assert np.allclose(out[2], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[3], np.array([[-1, -5], [-2, -5.5]]))
#     assert np.allclose(out[4], np.array([[13, 56], [-14, -58.75]]))
#     assert np.allclose(out[5], np.array([[-57, -237.75], [51, 211.125]]))
#     assert np.allclose(out[6], np.array([[1626.75, -480.375], [-1441.125, 425.8125]]))


# def test_workflow_multiply_topheavy_complicated_zero_handler_three_consumer_processes():
#     inp0 = Input(a=np.array([[1, 2], [2, 1]]))
#     inp1 = Input(a=np.array([[-3, 1], [-3, 0.5]]))
#     handler = NegativeDetHandler(requires_kw="a")
#     mm0, mm1, mm2, mm3, mm4, mm5 = (
#         MatMul(handlers=[handler]),
#         MatMul(handlers=[handler]),
#         MatMul(handlers=[handler]),
#         MatMul(handlers=[handler]),
#         MatMul(handlers=[handler]),
#         MatMul(handlers=[handler]),
#     )
#     mm0.requires(a=inp0, b=inp1)
#     mm1.requires(a=inp0, b=mm0)
#     mm2.requires(a=inp0, b=inp1)
#     mm3.requires(a=inp0, b=inp1)
#     mm4.requires(a=inp0, b=inp1)
#     mm5.requires(mm0, mm1, mm2, a=mm3, b=mm4)
#     out = materia.Workflow(inp0, inp1, mm0, mm1, mm2, mm3, mm4, mm5).run(
#         num_consumers=3, thread=False
#     )

#     assert set(out.keys()) == set((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12))
#     assert np.allclose(out[0], np.array([[1, 2], [2, 1]]))
#     assert np.allclose(out[1], np.array([[-3, 1], [-3, 0.5]]))
#     assert np.allclose(out[2], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[3], np.array([[-9, 3], [9, -1.5]]))
#     assert np.allclose(out[4], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[5], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[6], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[7], np.array([[99, -23], [-103.5, 24.25]]))
#     assert np.allclose(out[8], np.array([[9, -2], [-9, 2.5]]))
#     assert np.allclose(out[9], np.array([[9, -2], [-9, 2.5]]))
#     assert np.allclose(out[10], np.array([[9, -2], [-9, 2.5]]))
#     assert np.allclose(out[11], np.array([[9, -2], [-9, 2.5]]))
#     assert np.allclose(out[12], np.array([[9, -3], [9, -1.5]]))


# def test_workflow_slow_signal_complicated_success_handler_one_consumer_thread():
#     t0, t1, t2, t3, t4, t5, t6 = (
#         SlowSignal(handlers=[SuccessHandler()]),
#         SlowSignal(handlers=[SuccessHandler()]),
#         SlowSignal(handlers=[SuccessHandler()]),
#         SlowSignal(handlers=[SuccessHandler()]),
#         SlowSignal(handlers=[SuccessHandler()]),
#         SlowSignal(handlers=[SuccessHandler()]),
#         SlowSignal(handlers=[SuccessHandler()]),
#     )

#     t1.requires(t0)
#     t2.requires(t1)
#     t4.requires(t3)
#     t5.requires(t4)
#     t6.requires(t2, t5)

#     out = materia.Workflow(t0, t1, t2, t3, t4, t5, t6).run(num_consumers=1, thread=True)

#     assert out == {
#         0: "Signal triggered successfully.",
#         3: "Signal triggered successfully.",
#         7: "AddOn triggered successfully.",
#         8: "AddOn triggered successfully.",
#         1: "Signal triggered successfully.",
#         4: "Signal triggered successfully.",
#         9: "AddOn triggered successfully.",
#         10: "AddOn triggered successfully.",
#         2: "Signal triggered successfully.",
#         5: "Signal triggered successfully.",
#         11: "AddOn triggered successfully.",
#         12: "AddOn triggered successfully.",
#         6: "Signal triggered successfully.",
#         13: "AddOn triggered successfully.",
#     }


# def test_workflow_slow_multiply_linear_one_consumer_thread():
#     inp0 = Input(a=np.array([[1, 2], [2, 1]]))
#     inp1 = Input(a=np.array([[-3, 1], [-3, 0.5]]))
#     mm0, mm1, mm2 = SlowMatMul(), SlowMatMul(), SlowMatMul()
#     mm0.requires(a=inp0, b=inp1)
#     mm1.requires(a=inp1, b=inp0)
#     mm2.requires(a=mm0, b=mm1)
#     out = materia.Workflow(inp0, inp1, mm0, mm1, mm2).run(num_consumers=1, thread=True)

#     assert set(out.keys()) == set((0, 1, 2, 3, 4))
#     assert np.allclose(out[0], np.array([[1, 2], [2, 1]]))
#     assert np.allclose(out[1], np.array([[-3, 1], [-3, 0.5]]))
#     assert np.allclose(out[2], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[3], np.array([[-1, -5], [-2, -5.5]]))
#     assert np.allclose(out[4], np.array([[5, 34], [4, 31.25]]))


# def test_workflow_slow_multiply_linear_zero_handler_one_consumer_thread():
#     inp0 = Input(a=np.array([[1, 2], [2, 1]]))
#     inp1 = Input(a=np.array([[-3, 1], [-3, 0.5]]))
#     handler = NegativeDetHandler(requires_kw="a")
#     mm0, mm1, mm2 = (
#         SlowMatMul(handlers=[handler]),
#         SlowMatMul(handlers=[handler]),
#         SlowMatMul(handlers=[handler]),
#     )
#     mm0.requires(a=inp0, b=inp1)
#     mm1.requires(a=inp1, b=inp0)
#     mm2.requires(a=mm0, b=mm1)
#     out = materia.Workflow(inp0, inp1, mm0, mm1, mm2).run(num_consumers=1, thread=True)

#     assert set(out.keys()) == set((0, 1, 2, 3, 4, 5, 6))
#     assert np.allclose(out[0], np.array([[1, 2], [2, 1]]))
#     assert np.allclose(out[1], np.array([[-3, 1], [-3, 0.5]]))
#     assert np.allclose(out[2], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[3], np.array([[-1, -5], [-2, -5.5]]))
#     assert np.allclose(out[4], np.array([[13, 56], [-14, -58.75]]))
#     assert np.allclose(out[5], np.array([[9, -2], [-9, 2.5]]))
#     assert np.allclose(out[6], np.array([[1, 5], [-2, -5.5]]))


# def test_workflow_slow_multiply_complicated_one_consumer_thread():
#     inp0 = Input(a=np.array([[1, 2], [2, 1]]))
#     inp1 = Input(a=np.array([[-3, 1], [-3, 0.5]]))
#     mm0, mm1, mm2, mm3, mm4 = (
#         SlowMatMul(),
#         SlowMatMul(),
#         SlowMatMul(),
#         SlowMatMul(),
#         SlowMatMul(),
#     )
#     mm0.requires(a=inp0, b=inp1)
#     mm1.requires(a=inp1, b=inp0)
#     mm2.requires(a=mm0, b=mm1)
#     mm3.requires(a=mm1, b=mm2)
#     mm4.requires(a=mm3, b=mm0)
#     out = materia.Workflow(inp0, inp1, mm0, mm1, mm2, mm3, mm4).run(
#         num_consumers=1, thread=True
#     )

#     assert set(out.keys()) == set((0, 1, 2, 3, 4, 5, 6))
#     assert np.allclose(out[0], np.array([[1, 2], [2, 1]]))
#     assert np.allclose(out[1], np.array([[-3, 1], [-3, 0.5]]))
#     assert np.allclose(out[2], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[3], np.array([[-1, -5], [-2, -5.5]]))
#     assert np.allclose(out[4], np.array([[5, 34], [4, 31.25]]))
#     assert np.allclose(out[5], np.array([[-25, -190.25], [-32, -239.875]]))
#     assert np.allclose(out[6], np.array([[1937.25, -525.625], [2446.875, -663.6875]]))


# def test_workflow_slow_multiply_complicated_zero_handler_one_consumer_thread():
#     inp0 = Input(a=np.array([[1, 2], [2, 1]]))
#     inp1 = Input(a=np.array([[-3, 1], [-3, 0.5]]))
#     handler = NegativeDetHandler(requires_kw="a")
#     mm0, mm1, mm2, mm3, mm4 = (
#         SlowMatMul(handlers=[handler]),
#         SlowMatMul(handlers=[handler]),
#         SlowMatMul(handlers=[handler]),
#         SlowMatMul(handlers=[handler]),
#         SlowMatMul(handlers=[handler]),
#     )
#     mm0.requires(a=inp0, b=inp1)
#     mm1.requires(a=inp1, b=inp0)
#     mm2.requires(a=mm0, b=mm1)
#     mm3.requires(a=mm1, b=mm2)
#     mm4.requires(a=mm3, b=mm0)
#     out = materia.Workflow(inp0, inp1, mm0, mm1, mm2, mm3, mm4).run(
#         num_consumers=1, thread=True
#     )

#     assert set(out.keys()) == set((0, 1, 2, 3, 4, 5, 6, 7, 8))
#     assert np.allclose(out[0], np.array([[1, 2], [2, 1]]))
#     assert np.allclose(out[1], np.array([[-3, 1], [-3, 0.5]]))
#     assert np.allclose(out[2], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[3], np.array([[-1, -5], [-2, -5.5]]))
#     assert np.allclose(out[4], np.array([[13, 56], [-14, -58.75]]))
#     assert np.allclose(out[5], np.array([[-57, -237.75], [51, 211.125]]))
#     assert np.allclose(out[6], np.array([[1626.75, -480.375], [-1441.125, 425.8125]]))


# def test_workflow_slow_multiply_topheavy_complicated_zero_handler_one_consumer_thread():
#     inp0 = Input(a=np.array([[1, 2], [2, 1]]))
#     inp1 = Input(a=np.array([[-3, 1], [-3, 0.5]]))
#     handler = NegativeDetHandler(requires_kw="a")
#     mm0, mm1, mm2, mm3, mm4, mm5 = (
#         SlowMatMul(handlers=[handler]),
#         SlowMatMul(handlers=[handler]),
#         SlowMatMul(handlers=[handler]),
#         SlowMatMul(handlers=[handler]),
#         SlowMatMul(handlers=[handler]),
#         SlowMatMul(handlers=[handler]),
#     )
#     mm0.requires(a=inp0, b=inp1)
#     mm1.requires(a=inp0, b=mm0)
#     mm2.requires(a=inp0, b=inp1)
#     mm3.requires(a=inp0, b=inp1)
#     mm4.requires(a=inp0, b=inp1)
#     mm5.requires(mm0, mm1, mm2, a=mm3, b=mm4)
#     out = materia.Workflow(inp0, inp1, mm0, mm1, mm2, mm3, mm4, mm5).run(
#         num_consumers=1, thread=True
#     )

#     assert set(out.keys()) == set((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12))
#     assert np.allclose(out[0], np.array([[1, 2], [2, 1]]))
#     assert np.allclose(out[1], np.array([[-3, 1], [-3, 0.5]]))
#     assert np.allclose(out[2], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[3], np.array([[-9, 3], [9, -1.5]]))
#     assert np.allclose(out[4], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[5], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[6], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[7], np.array([[99, -23], [-103.5, 24.25]]))
#     assert np.allclose(out[8], np.array([[9, -2], [-9, 2.5]]))
#     assert np.allclose(out[9], np.array([[9, -2], [-9, 2.5]]))
#     assert np.allclose(out[10], np.array([[9, -2], [-9, 2.5]]))
#     assert np.allclose(out[11], np.array([[9, -2], [-9, 2.5]]))
#     assert np.allclose(out[12], np.array([[9, -3], [9, -1.5]]))


# def test_workflow_slow_signal_complicated_success_handler_two_consumer_threads():
#     t0, t1, t2, t3, t4, t5, t6 = (
#         SlowSignal(handlers=[SuccessHandler()]),
#         SlowSignal(handlers=[SuccessHandler()]),
#         SlowSignal(handlers=[SuccessHandler()]),
#         SlowSignal(handlers=[SuccessHandler()]),
#         SlowSignal(handlers=[SuccessHandler()]),
#         SlowSignal(handlers=[SuccessHandler()]),
#         SlowSignal(handlers=[SuccessHandler()]),
#     )

#     t1.requires(t0)
#     t2.requires(t1)
#     t4.requires(t3)
#     t5.requires(t4)
#     t6.requires(t2, t5)

#     out = materia.Workflow(t0, t1, t2, t3, t4, t5, t6).run(num_consumers=2, thread=True)

#     assert out == {
#         0: "Signal triggered successfully.",
#         3: "Signal triggered successfully.",
#         7: "AddOn triggered successfully.",
#         8: "AddOn triggered successfully.",
#         1: "Signal triggered successfully.",
#         4: "Signal triggered successfully.",
#         9: "AddOn triggered successfully.",
#         10: "AddOn triggered successfully.",
#         2: "Signal triggered successfully.",
#         5: "Signal triggered successfully.",
#         11: "AddOn triggered successfully.",
#         12: "AddOn triggered successfully.",
#         6: "Signal triggered successfully.",
#         13: "AddOn triggered successfully.",
#     }


# def test_workflow_slow_multiply_linear_two_consumer_threads():
#     inp0 = Input(a=np.array([[1, 2], [2, 1]]))
#     inp1 = Input(a=np.array([[-3, 1], [-3, 0.5]]))
#     mm0, mm1, mm2 = SlowMatMul(), SlowMatMul(), SlowMatMul()
#     mm0.requires(a=inp0, b=inp1)
#     mm1.requires(a=inp1, b=inp0)
#     mm2.requires(a=mm0, b=mm1)
#     out = materia.Workflow(inp0, inp1, mm0, mm1, mm2).run(num_consumers=2, thread=True)

#     assert set(out.keys()) == set((0, 1, 2, 3, 4))
#     assert np.allclose(out[0], np.array([[1, 2], [2, 1]]))
#     assert np.allclose(out[1], np.array([[-3, 1], [-3, 0.5]]))
#     assert np.allclose(out[2], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[3], np.array([[-1, -5], [-2, -5.5]]))
#     assert np.allclose(out[4], np.array([[5, 34], [4, 31.25]]))


# def test_workflow_slow_multiply_linear_zero_handler_two_consumer_threads():
#     inp0 = Input(a=np.array([[1, 2], [2, 1]]))
#     inp1 = Input(a=np.array([[-3, 1], [-3, 0.5]]))
#     handler = NegativeDetHandler(requires_kw="a")
#     mm0, mm1, mm2 = (
#         SlowMatMul(handlers=[handler]),
#         SlowMatMul(handlers=[handler]),
#         SlowMatMul(handlers=[handler]),
#     )
#     mm0.requires(a=inp0, b=inp1)
#     mm1.requires(a=inp1, b=inp0)
#     mm2.requires(a=mm0, b=mm1)
#     out = materia.Workflow(inp0, inp1, mm0, mm1, mm2).run(num_consumers=2, thread=True)

#     assert set(out.keys()) == set((0, 1, 2, 3, 4, 5, 6))
#     assert np.allclose(out[0], np.array([[1, 2], [2, 1]]))
#     assert np.allclose(out[1], np.array([[-3, 1], [-3, 0.5]]))
#     assert np.allclose(out[2], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[3], np.array([[-1, -5], [-2, -5.5]]))
#     assert np.allclose(out[4], np.array([[13, 56], [-14, -58.75]]))
#     assert (
#         np.allclose(out[5], np.array([[9, -2], [-9, 2.5]]))
#         and np.allclose(out[6], np.array([[1, 5], [-2, -5.5]]))
#     ) or (
#         np.allclose(out[6], np.array([[9, -2], [-9, 2.5]]))
#         and np.allclose(out[5], np.array([[1, 5], [-2, -5.5]]))
#     )


# def test_workflow_slow_multiply_complicated_two_consumer_threads():
#     inp0 = Input(a=np.array([[1, 2], [2, 1]]))
#     inp1 = Input(a=np.array([[-3, 1], [-3, 0.5]]))
#     mm0, mm1, mm2, mm3, mm4 = (
#         SlowMatMul(),
#         SlowMatMul(),
#         SlowMatMul(),
#         SlowMatMul(),
#         SlowMatMul(),
#     )
#     mm0.requires(a=inp0, b=inp1)
#     mm1.requires(a=inp1, b=inp0)
#     mm2.requires(a=mm0, b=mm1)
#     mm3.requires(a=mm1, b=mm2)
#     mm4.requires(a=mm3, b=mm0)
#     out = materia.Workflow(inp0, inp1, mm0, mm1, mm2, mm3, mm4).run(
#         num_consumers=2, thread=True
#     )

#     assert set(out.keys()) == set((0, 1, 2, 3, 4, 5, 6))
#     assert np.allclose(out[0], np.array([[1, 2], [2, 1]]))
#     assert np.allclose(out[1], np.array([[-3, 1], [-3, 0.5]]))
#     assert np.allclose(out[2], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[3], np.array([[-1, -5], [-2, -5.5]]))
#     assert np.allclose(out[4], np.array([[5, 34], [4, 31.25]]))
#     assert np.allclose(out[5], np.array([[-25, -190.25], [-32, -239.875]]))
#     assert np.allclose(out[6], np.array([[1937.25, -525.625], [2446.875, -663.6875]]))


# def test_workflow_slow_multiply_complicated_zero_handler_two_consumer_threads():
#     inp0 = Input(a=np.array([[1, 2], [2, 1]]))
#     inp1 = Input(a=np.array([[-3, 1], [-3, 0.5]]))
#     handler = NegativeDetHandler(requires_kw="a")
#     mm0, mm1, mm2, mm3, mm4 = (
#         SlowMatMul(handlers=[handler]),
#         SlowMatMul(handlers=[handler]),
#         SlowMatMul(handlers=[handler]),
#         SlowMatMul(handlers=[handler]),
#         SlowMatMul(handlers=[handler]),
#     )
#     mm0.requires(a=inp0, b=inp1)
#     mm1.requires(a=inp1, b=inp0)
#     mm2.requires(a=mm0, b=mm1)
#     mm3.requires(a=mm1, b=mm2)
#     mm4.requires(a=mm3, b=mm0)
#     out = materia.Workflow(inp0, inp1, mm0, mm1, mm2, mm3, mm4).run(
#         num_consumers=2, thread=True
#     )

#     assert set(out.keys()) == set((0, 1, 2, 3, 4, 5, 6, 7, 8))
#     assert np.allclose(out[0], np.array([[1, 2], [2, 1]]))
#     assert np.allclose(out[1], np.array([[-3, 1], [-3, 0.5]]))
#     assert np.allclose(out[2], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[3], np.array([[-1, -5], [-2, -5.5]]))
#     assert np.allclose(out[4], np.array([[13, 56], [-14, -58.75]]))
#     assert np.allclose(out[5], np.array([[-57, -237.75], [51, 211.125]]))
#     assert np.allclose(out[6], np.array([[1626.75, -480.375], [-1441.125, 425.8125]]))


# def test_workflow_slow_multiply_topheavy_complicated_zero_handler_two_consumer_threads():
#     inp0 = Input(a=np.array([[1, 2], [2, 1]]))
#     inp1 = Input(a=np.array([[-3, 1], [-3, 0.5]]))
#     handler = NegativeDetHandler(requires_kw="a")
#     mm0, mm1, mm2, mm3, mm4, mm5 = (
#         SlowMatMul(handlers=[handler]),
#         SlowMatMul(handlers=[handler]),
#         SlowMatMul(handlers=[handler]),
#         SlowMatMul(handlers=[handler]),
#         SlowMatMul(handlers=[handler]),
#         SlowMatMul(handlers=[handler]),
#     )
#     mm0.requires(a=inp0, b=inp1)
#     mm1.requires(a=inp0, b=mm0)
#     mm2.requires(a=inp0, b=inp1)
#     mm3.requires(a=inp0, b=inp1)
#     mm4.requires(a=inp0, b=inp1)
#     mm5.requires(mm0, mm1, mm2, a=mm3, b=mm4)
#     out = materia.Workflow(inp0, inp1, mm0, mm1, mm2, mm3, mm4, mm5).run(
#         num_consumers=2, thread=True
#     )

#     assert set(out.keys()) == set((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12))
#     assert np.allclose(out[0], np.array([[1, 2], [2, 1]]))
#     assert np.allclose(out[1], np.array([[-3, 1], [-3, 0.5]]))
#     assert np.allclose(out[2], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[3], np.array([[-9, 3], [9, -1.5]]))
#     assert np.allclose(out[4], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[5], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[6], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[7], np.array([[99, -23], [-103.5, 24.25]]))
#     assert np.allclose(out[8], np.array([[9, -2], [-9, 2.5]]))
#     assert np.allclose(out[9], np.array([[9, -2], [-9, 2.5]]))
#     assert np.allclose(out[10], np.array([[9, -2], [-9, 2.5]]))
#     assert np.allclose(out[11], np.array([[9, -2], [-9, 2.5]]))
#     assert np.allclose(out[12], np.array([[9, -3], [9, -1.5]]))


# def test_workflow_slow_signal_complicated_success_handler_three_consumer_threads():
#     t0, t1, t2, t3, t4, t5, t6 = (
#         SlowSignal(handlers=[SuccessHandler()]),
#         SlowSignal(handlers=[SuccessHandler()]),
#         SlowSignal(handlers=[SuccessHandler()]),
#         SlowSignal(handlers=[SuccessHandler()]),
#         SlowSignal(handlers=[SuccessHandler()]),
#         SlowSignal(handlers=[SuccessHandler()]),
#         SlowSignal(handlers=[SuccessHandler()]),
#     )

#     t1.requires(t0)
#     t2.requires(t1)
#     t4.requires(t3)
#     t5.requires(t4)
#     t6.requires(t2, t5)

#     out = materia.Workflow(t0, t1, t2, t3, t4, t5, t6).run(num_consumers=3, thread=True)

#     assert out == {
#         0: "Signal triggered successfully.",
#         3: "Signal triggered successfully.",
#         7: "AddOn triggered successfully.",
#         8: "AddOn triggered successfully.",
#         1: "Signal triggered successfully.",
#         4: "Signal triggered successfully.",
#         9: "AddOn triggered successfully.",
#         10: "AddOn triggered successfully.",
#         2: "Signal triggered successfully.",
#         5: "Signal triggered successfully.",
#         11: "AddOn triggered successfully.",
#         12: "AddOn triggered successfully.",
#         6: "Signal triggered successfully.",
#         13: "AddOn triggered successfully.",
#     }


# def test_workflow_slow_multiply_linear_three_consumer_threads():
#     inp0 = Input(a=np.array([[1, 2], [2, 1]]))
#     inp1 = Input(a=np.array([[-3, 1], [-3, 0.5]]))
#     mm0, mm1, mm2 = SlowMatMul(), SlowMatMul(), SlowMatMul()
#     mm0.requires(a=inp0, b=inp1)
#     mm1.requires(a=inp1, b=inp0)
#     mm2.requires(a=mm0, b=mm1)
#     out = materia.Workflow(inp0, inp1, mm0, mm1, mm2).run(num_consumers=3, thread=True)

#     assert set(out.keys()) == set((0, 1, 2, 3, 4))
#     assert np.allclose(out[0], np.array([[1, 2], [2, 1]]))
#     assert np.allclose(out[1], np.array([[-3, 1], [-3, 0.5]]))
#     assert np.allclose(out[2], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[3], np.array([[-1, -5], [-2, -5.5]]))
#     assert np.allclose(out[4], np.array([[5, 34], [4, 31.25]]))


# def test_workflow_slow_multiply_linear_zero_handler_three_consumer_threads():
#     inp0 = Input(a=np.array([[1, 2], [2, 1]]))
#     inp1 = Input(a=np.array([[-3, 1], [-3, 0.5]]))
#     handler = NegativeDetHandler(requires_kw="a")
#     mm0, mm1, mm2 = (
#         SlowMatMul(handlers=[handler]),
#         SlowMatMul(handlers=[handler]),
#         SlowMatMul(handlers=[handler]),
#     )
#     mm0.requires(a=inp0, b=inp1)
#     mm1.requires(a=inp1, b=inp0)
#     mm2.requires(a=mm0, b=mm1)
#     out = materia.Workflow(inp0, inp1, mm0, mm1, mm2).run(num_consumers=3, thread=True)

#     assert set(out.keys()) == set((0, 1, 2, 3, 4, 5, 6))
#     assert np.allclose(out[0], np.array([[1, 2], [2, 1]]))
#     assert np.allclose(out[1], np.array([[-3, 1], [-3, 0.5]]))
#     assert np.allclose(out[2], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[3], np.array([[-1, -5], [-2, -5.5]]))
#     assert np.allclose(out[4], np.array([[13, 56], [-14, -58.75]]))
#     assert (
#         np.allclose(out[5], np.array([[9, -2], [-9, 2.5]]))
#         and np.allclose(out[6], np.array([[1, 5], [-2, -5.5]]))
#     ) or (
#         np.allclose(out[6], np.array([[9, -2], [-9, 2.5]]))
#         and np.allclose(out[5], np.array([[1, 5], [-2, -5.5]]))
#     )


# def test_workflow_slow_multiply_complicated_three_consumer_threads():
#     inp0 = Input(a=np.array([[1, 2], [2, 1]]))
#     inp1 = Input(a=np.array([[-3, 1], [-3, 0.5]]))
#     mm0, mm1, mm2, mm3, mm4 = (
#         SlowMatMul(),
#         SlowMatMul(),
#         SlowMatMul(),
#         SlowMatMul(),
#         SlowMatMul(),
#     )
#     mm0.requires(a=inp0, b=inp1)
#     mm1.requires(a=inp1, b=inp0)
#     mm2.requires(a=mm0, b=mm1)
#     mm3.requires(a=mm1, b=mm2)
#     mm4.requires(a=mm3, b=mm0)
#     out = materia.Workflow(inp0, inp1, mm0, mm1, mm2, mm3, mm4).run(
#         num_consumers=3, thread=True
#     )

#     assert set(out.keys()) == set((0, 1, 2, 3, 4, 5, 6))
#     assert np.allclose(out[0], np.array([[1, 2], [2, 1]]))
#     assert np.allclose(out[1], np.array([[-3, 1], [-3, 0.5]]))
#     assert np.allclose(out[2], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[3], np.array([[-1, -5], [-2, -5.5]]))
#     assert np.allclose(out[4], np.array([[5, 34], [4, 31.25]]))
#     assert np.allclose(out[5], np.array([[-25, -190.25], [-32, -239.875]]))
#     assert np.allclose(out[6], np.array([[1937.25, -525.625], [2446.875, -663.6875]]))


# def test_workflow_slow_multiply_complicated_zero_handler_three_consumer_threads():
#     inp0 = Input(a=np.array([[1, 2], [2, 1]]))
#     inp1 = Input(a=np.array([[-3, 1], [-3, 0.5]]))
#     handler = NegativeDetHandler(requires_kw="a")
#     mm0, mm1, mm2, mm3, mm4 = (
#         SlowMatMul(handlers=[handler]),
#         SlowMatMul(handlers=[handler]),
#         SlowMatMul(handlers=[handler]),
#         SlowMatMul(handlers=[handler]),
#         SlowMatMul(handlers=[handler]),
#     )
#     mm0.requires(a=inp0, b=inp1)
#     mm1.requires(a=inp1, b=inp0)
#     mm2.requires(a=mm0, b=mm1)
#     mm3.requires(a=mm1, b=mm2)
#     mm4.requires(a=mm3, b=mm0)
#     out = materia.Workflow(inp0, inp1, mm0, mm1, mm2, mm3, mm4).run(
#         num_consumers=3, thread=True
#     )

#     assert set(out.keys()) == set((0, 1, 2, 3, 4, 5, 6, 7, 8))
#     assert np.allclose(out[0], np.array([[1, 2], [2, 1]]))
#     assert np.allclose(out[1], np.array([[-3, 1], [-3, 0.5]]))
#     assert np.allclose(out[2], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[3], np.array([[-1, -5], [-2, -5.5]]))
#     assert np.allclose(out[4], np.array([[13, 56], [-14, -58.75]]))
#     assert np.allclose(out[5], np.array([[-57, -237.75], [51, 211.125]]))
#     assert np.allclose(out[6], np.array([[1626.75, -480.375], [-1441.125, 425.8125]]))


# def test_workflow_slow_multiply_topheavy_complicated_zero_handler_three_consumer_threads():
#     # FIXME: this test has failed seemingly spontaneously before...
#     #     def test_workflow_slow_multiply_topheavy_complicated_zero_handler_three_consumer_threads():
#     #         inp0 = Input(a=np.array([[1, 2], [2, 1]]))
#     #         inp1 = Input(a=np.array([[-3, 1], [-3, 0.5]]))
#     #         handler = NegativeDetHandler(requires_kw="a")
#     #         mm0, mm1, mm2, mm3, mm4, mm5 = (
#     #             SlowMatMul(handlers=[handler]),
#     #             SlowMatMul(handlers=[handler]),
#     #             SlowMatMul(handlers=[handler]),
#     #             SlowMatMul(handlers=[handler]),
#     #             SlowMatMul(handlers=[handler]),
#     #             SlowMatMul(handlers=[handler]),
#     #         )
#     #         mm0.requires(a=inp0, b=inp1)
#     #         mm1.requires(a=inp0, b=mm0)
#     #         mm2.requires(a=inp0, b=inp1)
#     #         mm3.requires(a=inp0, b=inp1)
#     #         mm4.requires(a=inp0, b=inp1)
#     #         mm5.requires(mm0, mm1, mm2, a=mm3, b=mm4)
#     #         out = materia.Workflow(inp0, inp1, mm0, mm1, mm2, mm3, mm4, mm5).run(num_consumers=3, thread=True)
#     #
#     #         assert set(out.keys()) == set((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12))
#     #         assert np.allclose(out[0], np.array([[1, 2], [2, 1]]))
#     #         assert np.allclose(out[1], np.array([[-3, 1], [-3, 0.5]]))
#     #         assert np.allclose(out[2], np.array([[-9, 2], [-9, 2.5]]))
#     #         assert np.allclose(out[3], np.array([[-9, 3], [9, -1.5]]))
#     #         assert np.allclose(out[4], np.array([[-9, 2], [-9, 2.5]]))
#     #         assert np.allclose(out[5], np.array([[-9, 2], [-9, 2.5]]))
#     #         assert np.allclose(out[6], np.array([[-9, 2], [-9, 2.5]]))
#     #         assert np.allclose(out[7], np.array([[99, -23], [-103.5, 24.25]]))
#     #         assert np.allclose(out[8], np.array([[9, -2], [-9, 2.5]]))
#     #         assert np.allclose(out[9], np.array([[9, -2], [-9, 2.5]]))
#     #         assert np.allclose(out[10], np.array([[9, -2], [-9, 2.5]]))
#     # >       assert np.allclose(out[11], np.array([[9, -2], [-9, 2.5]]))
#     # E       assert False
#     # E        +  where False = <function allclose at 0x7fe223634ef0>(array([[ 9. , -3. ],\n       [ 9. , -1.5]]), array([[ 9. , -2. ],\n       [-9. ,  2.5]]))
#     # E        +    where <function allclose at 0x7fe223634ef0> = np.allclose
#     # E        +    and   array([[ 9. , -2. ],\n       [-9. ,  2.5]]) = <built-in function array>([[9, -2], [-9, 2.5]])
#     # E        +      where <built-in function array> = np.array
#     #
#     # tests/test_workflow.py:1664: AssertionError
#     inp0 = Input(a=np.array([[1, 2], [2, 1]]))
#     inp1 = Input(a=np.array([[-3, 1], [-3, 0.5]]))
#     handler = NegativeDetHandler(requires_kw="a")
#     mm0, mm1, mm2, mm3, mm4, mm5 = (
#         SlowMatMul(handlers=[handler]),
#         SlowMatMul(handlers=[handler]),
#         SlowMatMul(handlers=[handler]),
#         SlowMatMul(handlers=[handler]),
#         SlowMatMul(handlers=[handler]),
#         SlowMatMul(handlers=[handler]),
#     )
#     mm0.requires(a=inp0, b=inp1)
#     mm1.requires(a=inp0, b=mm0)
#     mm2.requires(a=inp0, b=inp1)
#     mm3.requires(a=inp0, b=inp1)
#     mm4.requires(a=inp0, b=inp1)
#     mm5.requires(mm0, mm1, mm2, a=mm3, b=mm4)
#     out = materia.Workflow(inp0, inp1, mm0, mm1, mm2, mm3, mm4, mm5).run(
#         num_consumers=3, thread=True
#     )

#     assert set(out.keys()) == set((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12))
#     assert np.allclose(out[0], np.array([[1, 2], [2, 1]]))
#     assert np.allclose(out[1], np.array([[-3, 1], [-3, 0.5]]))
#     assert np.allclose(out[2], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[3], np.array([[-9, 3], [9, -1.5]]))
#     assert np.allclose(out[4], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[5], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[6], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[7], np.array([[99, -23], [-103.5, 24.25]]))
#     assert np.allclose(out[8], np.array([[9, -2], [-9, 2.5]]))
#     assert np.allclose(out[9], np.array([[9, -2], [-9, 2.5]]))
#     assert np.allclose(out[10], np.array([[9, -2], [-9, 2.5]]))
#     assert np.allclose(out[11], np.array([[9, -2], [-9, 2.5]]))
#     assert np.allclose(out[12], np.array([[9, -3], [9, -1.5]]))


# def test_workflow_slow_signal_complicated_success_handler_one_consumer_process():
#     t0, t1, t2, t3, t4, t5, t6 = (
#         SlowSignal(handlers=[SuccessHandler()]),
#         SlowSignal(handlers=[SuccessHandler()]),
#         SlowSignal(handlers=[SuccessHandler()]),
#         SlowSignal(handlers=[SuccessHandler()]),
#         SlowSignal(handlers=[SuccessHandler()]),
#         SlowSignal(handlers=[SuccessHandler()]),
#         SlowSignal(handlers=[SuccessHandler()]),
#     )

#     t1.requires(t0)
#     t2.requires(t1)
#     t4.requires(t3)
#     t5.requires(t4)
#     t6.requires(t2, t5)

#     out = materia.Workflow(t0, t1, t2, t3, t4, t5, t6).run(num_consumers=1, thread=False)

#     assert out == {
#         0: "Signal triggered successfully.",
#         3: "Signal triggered successfully.",
#         7: "AddOn triggered successfully.",
#         8: "AddOn triggered successfully.",
#         1: "Signal triggered successfully.",
#         4: "Signal triggered successfully.",
#         9: "AddOn triggered successfully.",
#         10: "AddOn triggered successfully.",
#         2: "Signal triggered successfully.",
#         5: "Signal triggered successfully.",
#         11: "AddOn triggered successfully.",
#         12: "AddOn triggered successfully.",
#         6: "Signal triggered successfully.",
#         13: "AddOn triggered successfully.",
#     }


# def test_workflow_slow_multiply_linear_one_consumer_process():
#     inp0 = Input(a=np.array([[1, 2], [2, 1]]))
#     inp1 = Input(a=np.array([[-3, 1], [-3, 0.5]]))
#     mm0, mm1, mm2 = SlowMatMul(), SlowMatMul(), SlowMatMul()
#     mm0.requires(a=inp0, b=inp1)
#     mm1.requires(a=inp1, b=inp0)
#     mm2.requires(a=mm0, b=mm1)
#     out = materia.Workflow(inp0, inp1, mm0, mm1, mm2).run(num_consumers=1, thread=False)

#     assert set(out.keys()) == set((0, 1, 2, 3, 4))
#     assert np.allclose(out[0], np.array([[1, 2], [2, 1]]))
#     assert np.allclose(out[1], np.array([[-3, 1], [-3, 0.5]]))
#     assert np.allclose(out[2], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[3], np.array([[-1, -5], [-2, -5.5]]))
#     assert np.allclose(out[4], np.array([[5, 34], [4, 31.25]]))


# def test_workflow_slow_multiply_linear_zero_handler_one_consumer_process():
#     inp0 = Input(a=np.array([[1, 2], [2, 1]]))
#     inp1 = Input(a=np.array([[-3, 1], [-3, 0.5]]))
#     handler = NegativeDetHandler(requires_kw="a")
#     mm0, mm1, mm2 = (
#         SlowMatMul(handlers=[handler]),
#         SlowMatMul(handlers=[handler]),
#         SlowMatMul(handlers=[handler]),
#     )
#     mm0.requires(a=inp0, b=inp1)
#     mm1.requires(a=inp1, b=inp0)
#     mm2.requires(a=mm0, b=mm1)
#     out = materia.Workflow(inp0, inp1, mm0, mm1, mm2).run(num_consumers=1, thread=False)

#     assert set(out.keys()) == set((0, 1, 2, 3, 4, 5, 6))
#     assert np.allclose(out[0], np.array([[1, 2], [2, 1]]))
#     assert np.allclose(out[1], np.array([[-3, 1], [-3, 0.5]]))
#     assert np.allclose(out[2], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[3], np.array([[-1, -5], [-2, -5.5]]))
#     assert np.allclose(out[4], np.array([[13, 56], [-14, -58.75]]))
#     assert np.allclose(out[5], np.array([[9, -2], [-9, 2.5]]))
#     assert np.allclose(out[6], np.array([[1, 5], [-2, -5.5]]))


# def test_workflow_slow_multiply_complicated_one_consumer_process():
#     inp0 = Input(a=np.array([[1, 2], [2, 1]]))
#     inp1 = Input(a=np.array([[-3, 1], [-3, 0.5]]))
#     mm0, mm1, mm2, mm3, mm4 = (
#         SlowMatMul(),
#         SlowMatMul(),
#         SlowMatMul(),
#         SlowMatMul(),
#         SlowMatMul(),
#     )
#     mm0.requires(a=inp0, b=inp1)
#     mm1.requires(a=inp1, b=inp0)
#     mm2.requires(a=mm0, b=mm1)
#     mm3.requires(a=mm1, b=mm2)
#     mm4.requires(a=mm3, b=mm0)
#     out = materia.Workflow(inp0, inp1, mm0, mm1, mm2, mm3, mm4).run(
#         num_consumers=1, thread=False
#     )

#     assert set(out.keys()) == set((0, 1, 2, 3, 4, 5, 6))
#     assert np.allclose(out[0], np.array([[1, 2], [2, 1]]))
#     assert np.allclose(out[1], np.array([[-3, 1], [-3, 0.5]]))
#     assert np.allclose(out[2], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[3], np.array([[-1, -5], [-2, -5.5]]))
#     assert np.allclose(out[4], np.array([[5, 34], [4, 31.25]]))
#     assert np.allclose(out[5], np.array([[-25, -190.25], [-32, -239.875]]))
#     assert np.allclose(out[6], np.array([[1937.25, -525.625], [2446.875, -663.6875]]))


# def test_workflow_slow_multiply_complicated_zero_handler_one_consumer_process():
#     inp0 = Input(a=np.array([[1, 2], [2, 1]]))
#     inp1 = Input(a=np.array([[-3, 1], [-3, 0.5]]))
#     handler = NegativeDetHandler(requires_kw="a")
#     mm0, mm1, mm2, mm3, mm4 = (
#         SlowMatMul(handlers=[handler]),
#         SlowMatMul(handlers=[handler]),
#         SlowMatMul(handlers=[handler]),
#         SlowMatMul(handlers=[handler]),
#         SlowMatMul(handlers=[handler]),
#     )
#     mm0.requires(a=inp0, b=inp1)
#     mm1.requires(a=inp1, b=inp0)
#     mm2.requires(a=mm0, b=mm1)
#     mm3.requires(a=mm1, b=mm2)
#     mm4.requires(a=mm3, b=mm0)
#     out = materia.Workflow(inp0, inp1, mm0, mm1, mm2, mm3, mm4).run(
#         num_consumers=1, thread=False
#     )

#     assert set(out.keys()) == set((0, 1, 2, 3, 4, 5, 6, 7, 8))
#     assert np.allclose(out[0], np.array([[1, 2], [2, 1]]))
#     assert np.allclose(out[1], np.array([[-3, 1], [-3, 0.5]]))
#     assert np.allclose(out[2], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[3], np.array([[-1, -5], [-2, -5.5]]))
#     assert np.allclose(out[4], np.array([[13, 56], [-14, -58.75]]))
#     assert np.allclose(out[5], np.array([[-57, -237.75], [51, 211.125]]))
#     assert np.allclose(out[6], np.array([[1626.75, -480.375], [-1441.125, 425.8125]]))


# def test_workflow_slow_multiply_topheavy_complicated_zero_handler_one_consumer_process():
#     inp0 = Input(a=np.array([[1, 2], [2, 1]]))
#     inp1 = Input(a=np.array([[-3, 1], [-3, 0.5]]))
#     handler = NegativeDetHandler(requires_kw="a")
#     mm0, mm1, mm2, mm3, mm4, mm5 = (
#         SlowMatMul(handlers=[handler]),
#         SlowMatMul(handlers=[handler]),
#         SlowMatMul(handlers=[handler]),
#         SlowMatMul(handlers=[handler]),
#         SlowMatMul(handlers=[handler]),
#         SlowMatMul(handlers=[handler]),
#     )
#     mm0.requires(a=inp0, b=inp1)
#     mm1.requires(a=inp0, b=mm0)
#     mm2.requires(a=inp0, b=inp1)
#     mm3.requires(a=inp0, b=inp1)
#     mm4.requires(a=inp0, b=inp1)
#     mm5.requires(mm0, mm1, mm2, a=mm3, b=mm4)
#     out = materia.Workflow(inp0, inp1, mm0, mm1, mm2, mm3, mm4, mm5).run(
#         num_consumers=1, thread=False
#     )

#     assert set(out.keys()) == set((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12))
#     assert np.allclose(out[0], np.array([[1, 2], [2, 1]]))
#     assert np.allclose(out[1], np.array([[-3, 1], [-3, 0.5]]))
#     assert np.allclose(out[2], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[3], np.array([[-9, 3], [9, -1.5]]))
#     assert np.allclose(out[4], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[5], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[6], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[7], np.array([[99, -23], [-103.5, 24.25]]))
#     assert np.allclose(out[8], np.array([[9, -2], [-9, 2.5]]))
#     assert np.allclose(out[9], np.array([[9, -2], [-9, 2.5]]))
#     assert np.allclose(out[10], np.array([[9, -2], [-9, 2.5]]))
#     assert np.allclose(out[11], np.array([[9, -2], [-9, 2.5]]))
#     assert np.allclose(out[12], np.array([[9, -3], [9, -1.5]]))


# def test_workflow_slow_signal_complicated_success_handler_two_consumer_processes():
#     t0, t1, t2, t3, t4, t5, t6 = (
#         SlowSignal(handlers=[SuccessHandler()]),
#         SlowSignal(handlers=[SuccessHandler()]),
#         SlowSignal(handlers=[SuccessHandler()]),
#         SlowSignal(handlers=[SuccessHandler()]),
#         SlowSignal(handlers=[SuccessHandler()]),
#         SlowSignal(handlers=[SuccessHandler()]),
#         SlowSignal(handlers=[SuccessHandler()]),
#     )

#     t1.requires(t0)
#     t2.requires(t1)
#     t4.requires(t3)
#     t5.requires(t4)
#     t6.requires(t2, t5)

#     out = materia.Workflow(t0, t1, t2, t3, t4, t5, t6).run(num_consumers=2, thread=False)

#     assert out == {
#         0: "Signal triggered successfully.",
#         3: "Signal triggered successfully.",
#         7: "AddOn triggered successfully.",
#         8: "AddOn triggered successfully.",
#         1: "Signal triggered successfully.",
#         4: "Signal triggered successfully.",
#         9: "AddOn triggered successfully.",
#         10: "AddOn triggered successfully.",
#         2: "Signal triggered successfully.",
#         5: "Signal triggered successfully.",
#         11: "AddOn triggered successfully.",
#         12: "AddOn triggered successfully.",
#         6: "Signal triggered successfully.",
#         13: "AddOn triggered successfully.",
#     }


# def test_workflow_slow_multiply_linear_two_consumer_processes():
#     inp0 = Input(a=np.array([[1, 2], [2, 1]]))
#     inp1 = Input(a=np.array([[-3, 1], [-3, 0.5]]))
#     mm0, mm1, mm2 = SlowMatMul(), SlowMatMul(), SlowMatMul()
#     mm0.requires(a=inp0, b=inp1)
#     mm1.requires(a=inp1, b=inp0)
#     mm2.requires(a=mm0, b=mm1)
#     out = materia.Workflow(inp0, inp1, mm0, mm1, mm2).run(num_consumers=2, thread=False)

#     assert set(out.keys()) == set((0, 1, 2, 3, 4))
#     assert np.allclose(out[0], np.array([[1, 2], [2, 1]]))
#     assert np.allclose(out[1], np.array([[-3, 1], [-3, 0.5]]))
#     assert np.allclose(out[2], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[3], np.array([[-1, -5], [-2, -5.5]]))
#     assert np.allclose(out[4], np.array([[5, 34], [4, 31.25]]))


# def test_workflow_slow_multiply_linear_zero_handler_two_consumer_processes():
#     inp0 = Input(a=np.array([[1, 2], [2, 1]]))
#     inp1 = Input(a=np.array([[-3, 1], [-3, 0.5]]))
#     handler = NegativeDetHandler(requires_kw="a")
#     mm0, mm1, mm2 = (
#         SlowMatMul(handlers=[handler]),
#         SlowMatMul(handlers=[handler]),
#         SlowMatMul(handlers=[handler]),
#     )
#     mm0.requires(a=inp0, b=inp1)
#     mm1.requires(a=inp1, b=inp0)
#     mm2.requires(a=mm0, b=mm1)
#     out = materia.Workflow(inp0, inp1, mm0, mm1, mm2).run(num_consumers=2, thread=False)

#     assert set(out.keys()) == set((0, 1, 2, 3, 4, 5, 6))
#     assert np.allclose(out[0], np.array([[1, 2], [2, 1]]))
#     assert np.allclose(out[1], np.array([[-3, 1], [-3, 0.5]]))
#     assert np.allclose(out[2], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[3], np.array([[-1, -5], [-2, -5.5]]))
#     assert np.allclose(out[4], np.array([[13, 56], [-14, -58.75]]))
#     assert (
#         np.allclose(out[5], np.array([[9, -2], [-9, 2.5]]))
#         and np.allclose(out[6], np.array([[1, 5], [-2, -5.5]]))
#     ) or (
#         np.allclose(out[6], np.array([[9, -2], [-9, 2.5]]))
#         and np.allclose(out[5], np.array([[1, 5], [-2, -5.5]]))
#     )


# def test_workflow_slow_multiply_complicated_two_consumer_processes():
#     inp0 = Input(a=np.array([[1, 2], [2, 1]]))
#     inp1 = Input(a=np.array([[-3, 1], [-3, 0.5]]))
#     mm0, mm1, mm2, mm3, mm4 = (
#         SlowMatMul(),
#         SlowMatMul(),
#         SlowMatMul(),
#         SlowMatMul(),
#         SlowMatMul(),
#     )
#     mm0.requires(a=inp0, b=inp1)
#     mm1.requires(a=inp1, b=inp0)
#     mm2.requires(a=mm0, b=mm1)
#     mm3.requires(a=mm1, b=mm2)
#     mm4.requires(a=mm3, b=mm0)
#     out = materia.Workflow(inp0, inp1, mm0, mm1, mm2, mm3, mm4).run(
#         num_consumers=2, thread=False
#     )

#     assert set(out.keys()) == set((0, 1, 2, 3, 4, 5, 6))
#     assert np.allclose(out[0], np.array([[1, 2], [2, 1]]))
#     assert np.allclose(out[1], np.array([[-3, 1], [-3, 0.5]]))
#     assert np.allclose(out[2], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[3], np.array([[-1, -5], [-2, -5.5]]))
#     assert np.allclose(out[4], np.array([[5, 34], [4, 31.25]]))
#     assert np.allclose(out[5], np.array([[-25, -190.25], [-32, -239.875]]))
#     assert np.allclose(out[6], np.array([[1937.25, -525.625], [2446.875, -663.6875]]))


# def test_workflow_slow_multiply_complicated_zero_handler_two_consumer_processes():
#     inp0 = Input(a=np.array([[1, 2], [2, 1]]))
#     inp1 = Input(a=np.array([[-3, 1], [-3, 0.5]]))
#     handler = NegativeDetHandler(requires_kw="a")
#     mm0, mm1, mm2, mm3, mm4 = (
#         SlowMatMul(handlers=[handler]),
#         SlowMatMul(handlers=[handler]),
#         SlowMatMul(handlers=[handler]),
#         SlowMatMul(handlers=[handler]),
#         SlowMatMul(handlers=[handler]),
#     )
#     mm0.requires(a=inp0, b=inp1)
#     mm1.requires(a=inp1, b=inp0)
#     mm2.requires(a=mm0, b=mm1)
#     mm3.requires(a=mm1, b=mm2)
#     mm4.requires(a=mm3, b=mm0)
#     out = materia.Workflow(inp0, inp1, mm0, mm1, mm2, mm3, mm4).run(
#         num_consumers=2, thread=False
#     )

#     assert set(out.keys()) == set((0, 1, 2, 3, 4, 5, 6, 7, 8))
#     assert np.allclose(out[0], np.array([[1, 2], [2, 1]]))
#     assert np.allclose(out[1], np.array([[-3, 1], [-3, 0.5]]))
#     assert np.allclose(out[2], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[3], np.array([[-1, -5], [-2, -5.5]]))
#     assert np.allclose(out[4], np.array([[13, 56], [-14, -58.75]]))
#     assert np.allclose(out[5], np.array([[-57, -237.75], [51, 211.125]]))
#     assert np.allclose(out[6], np.array([[1626.75, -480.375], [-1441.125, 425.8125]]))


# def test_workflow_slow_multiply_topheavy_complicated_zero_handler_two_consumer_processes():
#     inp0 = Input(a=np.array([[1, 2], [2, 1]]))
#     inp1 = Input(a=np.array([[-3, 1], [-3, 0.5]]))
#     handler = NegativeDetHandler(requires_kw="a")
#     mm0, mm1, mm2, mm3, mm4, mm5 = (
#         SlowMatMul(handlers=[handler]),
#         SlowMatMul(handlers=[handler]),
#         SlowMatMul(handlers=[handler]),
#         SlowMatMul(handlers=[handler]),
#         SlowMatMul(handlers=[handler]),
#         SlowMatMul(handlers=[handler]),
#     )
#     mm0.requires(a=inp0, b=inp1)
#     mm1.requires(a=inp0, b=mm0)
#     mm2.requires(a=inp0, b=inp1)
#     mm3.requires(a=inp0, b=inp1)
#     mm4.requires(a=inp0, b=inp1)
#     mm5.requires(mm0, mm1, mm2, a=mm3, b=mm4)
#     out = materia.Workflow(inp0, inp1, mm0, mm1, mm2, mm3, mm4, mm5).run(
#         num_consumers=2, thread=False
#     )

#     assert set(out.keys()) == set((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12))
#     assert np.allclose(out[0], np.array([[1, 2], [2, 1]]))
#     assert np.allclose(out[1], np.array([[-3, 1], [-3, 0.5]]))
#     assert np.allclose(out[2], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[3], np.array([[-9, 3], [9, -1.5]]))
#     assert np.allclose(out[4], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[5], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[6], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[7], np.array([[99, -23], [-103.5, 24.25]]))
#     assert np.allclose(out[8], np.array([[9, -2], [-9, 2.5]]))
#     assert np.allclose(out[9], np.array([[9, -2], [-9, 2.5]]))
#     assert np.allclose(out[10], np.array([[9, -2], [-9, 2.5]]))
#     assert np.allclose(out[11], np.array([[9, -2], [-9, 2.5]]))
#     assert np.allclose(out[12], np.array([[9, -3], [9, -1.5]]))


# def test_workflow_slow_signal_complicated_success_handler_three_consumer_processes():
#     t0, t1, t2, t3, t4, t5, t6 = (
#         SlowSignal(handlers=[SuccessHandler()]),
#         SlowSignal(handlers=[SuccessHandler()]),
#         SlowSignal(handlers=[SuccessHandler()]),
#         SlowSignal(handlers=[SuccessHandler()]),
#         SlowSignal(handlers=[SuccessHandler()]),
#         SlowSignal(handlers=[SuccessHandler()]),
#         SlowSignal(handlers=[SuccessHandler()]),
#     )

#     t1.requires(t0)
#     t2.requires(t1)
#     t4.requires(t3)
#     t5.requires(t4)
#     t6.requires(t2, t5)

#     out = materia.Workflow(t0, t1, t2, t3, t4, t5, t6).run(num_consumers=3, thread=False)

#     assert out == {
#         0: "Signal triggered successfully.",
#         3: "Signal triggered successfully.",
#         7: "AddOn triggered successfully.",
#         8: "AddOn triggered successfully.",
#         1: "Signal triggered successfully.",
#         4: "Signal triggered successfully.",
#         9: "AddOn triggered successfully.",
#         10: "AddOn triggered successfully.",
#         2: "Signal triggered successfully.",
#         5: "Signal triggered successfully.",
#         11: "AddOn triggered successfully.",
#         12: "AddOn triggered successfully.",
#         6: "Signal triggered successfully.",
#         13: "AddOn triggered successfully.",
#     }


# def test_workflow_slow_multiply_linear_three_consumer_processes():
#     inp0 = Input(a=np.array([[1, 2], [2, 1]]))
#     inp1 = Input(a=np.array([[-3, 1], [-3, 0.5]]))
#     mm0, mm1, mm2 = SlowMatMul(), SlowMatMul(), SlowMatMul()
#     mm0.requires(a=inp0, b=inp1)
#     mm1.requires(a=inp1, b=inp0)
#     mm2.requires(a=mm0, b=mm1)
#     out = materia.Workflow(inp0, inp1, mm0, mm1, mm2).run(num_consumers=3, thread=False)

#     assert set(out.keys()) == set((0, 1, 2, 3, 4))
#     assert np.allclose(out[0], np.array([[1, 2], [2, 1]]))
#     assert np.allclose(out[1], np.array([[-3, 1], [-3, 0.5]]))
#     assert np.allclose(out[2], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[3], np.array([[-1, -5], [-2, -5.5]]))
#     assert np.allclose(out[4], np.array([[5, 34], [4, 31.25]]))


# def test_workflow_slow_multiply_linear_zero_handler_three_consumer_processes():
#     inp0 = Input(a=np.array([[1, 2], [2, 1]]))
#     inp1 = Input(a=np.array([[-3, 1], [-3, 0.5]]))
#     handler = NegativeDetHandler(requires_kw="a")
#     mm0, mm1, mm2 = (
#         SlowMatMul(handlers=[handler]),
#         SlowMatMul(handlers=[handler]),
#         SlowMatMul(handlers=[handler]),
#     )
#     mm0.requires(a=inp0, b=inp1)
#     mm1.requires(a=inp1, b=inp0)
#     mm2.requires(a=mm0, b=mm1)
#     out = materia.Workflow(inp0, inp1, mm0, mm1, mm2).run(num_consumers=3, thread=False)

#     assert set(out.keys()) == set((0, 1, 2, 3, 4, 5, 6))
#     assert np.allclose(out[0], np.array([[1, 2], [2, 1]]))
#     assert np.allclose(out[1], np.array([[-3, 1], [-3, 0.5]]))
#     assert np.allclose(out[2], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[3], np.array([[-1, -5], [-2, -5.5]]))
#     assert np.allclose(out[4], np.array([[13, 56], [-14, -58.75]]))
#     assert (
#         np.allclose(out[5], np.array([[9, -2], [-9, 2.5]]))
#         and np.allclose(out[6], np.array([[1, 5], [-2, -5.5]]))
#     ) or (
#         np.allclose(out[6], np.array([[9, -2], [-9, 2.5]]))
#         and np.allclose(out[5], np.array([[1, 5], [-2, -5.5]]))
#     )


# def test_workflow_slow_multiply_complicated_three_consumer_processes():
#     inp0 = Input(a=np.array([[1, 2], [2, 1]]))
#     inp1 = Input(a=np.array([[-3, 1], [-3, 0.5]]))
#     mm0, mm1, mm2, mm3, mm4 = (
#         SlowMatMul(),
#         SlowMatMul(),
#         SlowMatMul(),
#         SlowMatMul(),
#         SlowMatMul(),
#     )
#     mm0.requires(a=inp0, b=inp1)
#     mm1.requires(a=inp1, b=inp0)
#     mm2.requires(a=mm0, b=mm1)
#     mm3.requires(a=mm1, b=mm2)
#     mm4.requires(a=mm3, b=mm0)
#     out = materia.Workflow(inp0, inp1, mm0, mm1, mm2, mm3, mm4).run(
#         num_consumers=3, thread=False
#     )

#     assert set(out.keys()) == set((0, 1, 2, 3, 4, 5, 6))
#     assert np.allclose(out[0], np.array([[1, 2], [2, 1]]))
#     assert np.allclose(out[1], np.array([[-3, 1], [-3, 0.5]]))
#     assert np.allclose(out[2], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[3], np.array([[-1, -5], [-2, -5.5]]))
#     assert np.allclose(out[4], np.array([[5, 34], [4, 31.25]]))
#     assert np.allclose(out[5], np.array([[-25, -190.25], [-32, -239.875]]))
#     assert np.allclose(out[6], np.array([[1937.25, -525.625], [2446.875, -663.6875]]))


# def test_workflow_slow_multiply_complicated_zero_handler_three_consumer_processes():
#     inp0 = Input(a=np.array([[1, 2], [2, 1]]))
#     inp1 = Input(a=np.array([[-3, 1], [-3, 0.5]]))
#     handler = NegativeDetHandler(requires_kw="a")
#     mm0, mm1, mm2, mm3, mm4 = (
#         SlowMatMul(handlers=[handler]),
#         SlowMatMul(handlers=[handler]),
#         SlowMatMul(handlers=[handler]),
#         SlowMatMul(handlers=[handler]),
#         SlowMatMul(handlers=[handler]),
#     )
#     mm0.requires(a=inp0, b=inp1)
#     mm1.requires(a=inp1, b=inp0)
#     mm2.requires(a=mm0, b=mm1)
#     mm3.requires(a=mm1, b=mm2)
#     mm4.requires(a=mm3, b=mm0)
#     out = materia.Workflow(inp0, inp1, mm0, mm1, mm2, mm3, mm4).run(
#         num_consumers=3, thread=False
#     )

#     assert set(out.keys()) == set((0, 1, 2, 3, 4, 5, 6, 7, 8))
#     assert np.allclose(out[0], np.array([[1, 2], [2, 1]]))
#     assert np.allclose(out[1], np.array([[-3, 1], [-3, 0.5]]))
#     assert np.allclose(out[2], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[3], np.array([[-1, -5], [-2, -5.5]]))
#     assert np.allclose(out[4], np.array([[13, 56], [-14, -58.75]]))
#     assert np.allclose(out[5], np.array([[-57, -237.75], [51, 211.125]]))
#     assert np.allclose(out[6], np.array([[1626.75, -480.375], [-1441.125, 425.8125]]))


# def test_workflow_slow_multiply_topheavy_complicated_zero_handler_three_consumer_processes():
#     inp0 = Input(a=np.array([[1, 2], [2, 1]]))
#     inp1 = Input(a=np.array([[-3, 1], [-3, 0.5]]))
#     handler = NegativeDetHandler(requires_kw="a")
#     mm0, mm1, mm2, mm3, mm4, mm5 = (
#         SlowMatMul(handlers=[handler]),
#         SlowMatMul(handlers=[handler]),
#         SlowMatMul(handlers=[handler]),
#         SlowMatMul(handlers=[handler]),
#         SlowMatMul(handlers=[handler]),
#         SlowMatMul(handlers=[handler]),
#     )
#     mm0.requires(a=inp0, b=inp1)
#     mm1.requires(a=inp0, b=mm0)
#     mm2.requires(a=inp0, b=inp1)
#     mm3.requires(a=inp0, b=inp1)
#     mm4.requires(a=inp0, b=inp1)
#     mm5.requires(mm0, mm1, mm2, a=mm3, b=mm4)
#     out = materia.Workflow(inp0, inp1, mm0, mm1, mm2, mm3, mm4, mm5).run(
#         num_consumers=3, thread=False
#     )

#     assert set(out.keys()) == set((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12))
#     assert np.allclose(out[0], np.array([[1, 2], [2, 1]]))
#     assert np.allclose(out[1], np.array([[-3, 1], [-3, 0.5]]))
#     assert np.allclose(out[2], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[3], np.array([[-9, 3], [9, -1.5]]))
#     assert np.allclose(out[4], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[5], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[6], np.array([[-9, 2], [-9, 2.5]]))
#     assert np.allclose(out[7], np.array([[99, -23], [-103.5, 24.25]]))
#     assert np.allclose(out[8], np.array([[9, -2], [-9, 2.5]]))
#     assert np.allclose(out[9], np.array([[9, -2], [-9, 2.5]]))
#     assert np.allclose(out[10], np.array([[9, -2], [-9, 2.5]]))
#     assert np.allclose(out[11], np.array([[9, -2], [-9, 2.5]]))
#     assert np.allclose(out[12], np.array([[9, -3], [9, -1.5]]))


# # import json
# # import os
# #
# # import materia
# #
# # class Append(materia.Task):
# #     def __init__(self, append_string, input_name, output_name, output_dir):
# #         self.settings['append_string'] = append_string
# #         self.settings['input_path'] = materia.utils.expand_path(os.path.join(output_dir,input_name))
# #         self.settings['output_path'] = materia.utils.expand_path(os.path.join(output_dir,output_name))
# #
# #     def run(self):
# #         with open(self.settings['input_path'],'r') as f:
# #             s = json.load(f)['s']
# #
# #         with open(self.settings['output_path'],'w') as f:
# #             json.dump({'result': s + self.append_string},f)
# #
# # class Combine:
# #     def __init__(self, input_name_1, input_name_2, output_name):
# #         self.settings['input_path_1'] = materia.utils.expand_path(os.path.join(output_dir,input_name_1))
# #         self.settings['input_path_2'] = materia.utils.expand_path(os.path.join(output_dir,input_name_2))
# #         self.settings['output_path'] = materia.utils.expand_path(os.path.join(output_dir,output_name))
# #
# #     def run(self):
# #         with open(os.path.join(self.output_dir,self.read_from_1),'r') as f:
# #             s1 = json.load(f)['result']
# #
# #         with open(os.path.join(self.output_dir,self.read_from_2),'r') as f:
# #             s2 = json.load(f)['result']
# #
# #         with open(os.path.join(self.output_dir,'combine.out'),'w') as f:
# #             json.dump({'result': s1 + s2},f)
# #
# # class FirstHalf:
# #     def __init__(self, read_from, output_dir):
# #         self.read_from = read_from
# #         self.output_dir = output_dir
# #
# #     def run(self):
# #         with open(os.path.join(self.output_dir,self.read_from),'r') as f:
# #             s = json.load(f)['s']
# #
# #         with open(os.path.join(self.output_dir,'first_half.out'),'w') as f:
# #             json.dump({'result': s[:len(s)//2]},f)
# #
# # class Reverse:
# #     def __init__(self, read_from, output_dir):
# #         self.read_from = read_from
# #         self.output_dir = output_dir
# #
# #     def run(self):
# #         with open(os.path.join(self.output_dir,self.read_from),'r') as f:
# #             s = json.load(f)['result']
# #
# #         with open(os.path.join(self.output_dir,'reverse.out'),'w') as f:
# #             json.dump({'result': s[::-1]},f)


# # import numpy as np
# #
# # import materia
# #
# # class Mul(materia.Task):
# #     def run(self, **kwargs):
# #         return {'product': np.random.randint(10)*np.random.randint(10)}
# #
# # class Signal(materia.Task):
# #     def run(self, **kwargs):
# #         return {'signal': 'ZeroHandler triggered successfully.'}
# #
# # class ZeroHandler(materia.Handler):
# #     def check(self, product):
# #         return product == 0
# #
# #     def handle(self, handle_list):#node, task, dag, done, enqueued):
# #         #return materia.Actions([materia.AddChildTask(node=node,task=task,dag=dag,child_task=Signal(),done=done,enqueued=enqueued),materia.Rerun(node=node,done=done)])
# #         return materia.Actions([materia.AddChildTask(handle_list=handle_list,child_task=Signal()),materia.Rerun(handle_list=handle_list)])
# #
# # def test_workflow_slow_multiply_linear():
# #     np.random.seed(10198735)
# #
# #     tasks = (Mul(),Mul(),Mul())
# #     links = {0:[1],1:[2],2:[]}
# #     wf = materia.Workflow(tasks=tasks,links=links)
# #
# #     assert wf.run(num_processors=2) == {0: {'product': 18}, 1: {'product': 16}, 2: {'product': 0}}
# #
# # def test_workflow_slow_multiply_linear_zero_handler():
# #     np.random.seed(10198735)
# #
# #     zh = [ZeroHandler()]
# #     tasks = (Mul(handlers=zh),Mul(handlers=zh),Mul(handlers=zh))
# #     links = {0:[1],1:[2],2:[]}
# #     wf = materia.Workflow(tasks=tasks,links=links)
# #
# #     assert wf.run(num_processors=2) == {0: {'product': 18}, 1: {'product': 16}, 2: {'product': 16}, 3: {'signal': 'ZeroHandler triggered successfully.'}}
# #
# # def test_workflow_slow_multiply_complicated():
# #     np.random.seed(10198735)
# #
# #     tasks = (Mul(),Mul(),Mul(),Mul(),Mul())
# #     links = {0:[2],1:[2],2:[3,4],3:[],4:[]}
# #     wf = materia.Workflow(tasks=tasks,links=links)
# #
# #     assert wf.run(num_processors=2) == {0: {'product': 18}, 1: {'product': 18}, 2: {'product': 16}, 3: {'product': 0}, 4: {'product': 16}}
# #
# # def test_workflow_slow_multiply_complicated_zero_handler():
# #     np.random.seed(10198735)
# #
# #     zh = [ZeroHandler()]
# #     tasks = (Mul(handlers=zh),Mul(handlers=zh),Mul(handlers=zh),Mul(handlers=zh),Mul(handlers=zh))
# #     links = {0:[2],1:[2],2:[3,4],3:[],4:[]}
# #     wf = materia.Workflow(tasks=tasks,links=links)
# #
# #     assert wf.run(num_processors=2) == {0: {'product': 18}, 1: {'product': 18}, 2: {'product': 16}, 3: {'product': 16}, 4: {'product': 16}, 5: {'signal': 'ZeroHandler triggered successfully.'}}
# #
# # # import json
# # # import os
# # #
# # # import materia
# # #
# # # class Append(materia.Task):
# # #     def __init__(self, append_string, input_name, output_name, output_dir):
# # #         self.settings['append_string'] = append_string
# # #         self.settings['input_path'] = materia.utils.expand_path(os.path.join(output_dir,input_name))
# # #         self.settings['output_path'] = materia.utils.expand_path(os.path.join(output_dir,output_name))
# # #
# # #     def run(self):
# # #         with open(self.settings['input_path'],'r') as f:
# # #             s = json.load(f)['s']
# # #
# # #         with open(self.settings['output_path'],'w') as f:
# # #             json.dump({'result': s + self.append_string},f)
# # #
# # # class Combine:
# # #     def __init__(self, input_name_1, input_name_2, output_name):
# # #         self.settings['input_path_1'] = materia.utils.expand_path(os.path.join(output_dir,input_name_1))
# # #         self.settings['input_path_2'] = materia.utils.expand_path(os.path.join(output_dir,input_name_2))
# # #         self.settings['output_path'] = materia.utils.expand_path(os.path.join(output_dir,output_name))
# # #
# # #     def run(self):
# # #         with open(os.path.join(self.output_dir,self.read_from_1),'r') as f:
# # #             s1 = json.load(f)['result']
# # #
# # #         with open(os.path.join(self.output_dir,self.read_from_2),'r') as f:
# # #             s2 = json.load(f)['result']
# # #
# # #         with open(os.path.join(self.output_dir,'combine.out'),'w') as f:
# # #             json.dump({'result': s1 + s2},f)
# # #
# # # class FirstHalf:
# # #     def __init__(self, read_from, output_dir):
# # #         self.read_from = read_from
# # #         self.output_dir = output_dir
# # #
# # #     def run(self):
# # #         with open(os.path.join(self.output_dir,self.read_from),'r') as f:
# # #             s = json.load(f)['s']
# # #
# # #         with open(os.path.join(self.output_dir,'first_half.out'),'w') as f:
# # #             json.dump({'result': s[:len(s)//2]},f)
# # #
# # # class Reverse:
# # #     def __init__(self, read_from, output_dir):
# # #         self.read_from = read_from
# # #         self.output_dir = output_dir
# # #
# # #     def run(self):
# # #         with open(os.path.join(self.output_dir,self.read_from),'r') as f:
# # #             s = json.load(f)['result']
# # #
# # #         with open(os.path.join(self.output_dir,'reverse.out'),'w') as f:
# # #             json.dump({'result': s[::-1]},f)
