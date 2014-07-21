package contable

import org.scalatest._
import breeze.linalg._

class TestMargins extends FunSpec {

  def m1 = new Margins(DenseVector(2,2,2,2),DenseVector(2,2,2,2))
  def m2 = new Margins(DenseVector(Range(0,5).toArray),DenseVector(Range(0,5).toArray))
  def m3 = new Margins(DenseVector(),DenseVector())
  def m4 = new Margins(DenseVector.fill[Int](4)(3), DenseVector.fill[Int](6)(2))
  def m5 = new Margins(DenseVector(3,1,3),DenseVector(2,3,4))
  def m6 = new Margins(DenseVector(10),DenseVector(Range(1,5).toArray))

  describe("A Margins") {
    it("should correctly determine feasibility") {
      assert(m1.isFeasible)
      assert(m2.isFeasible)
      assert(!m3.isFeasible)
      assert(m4.isFeasible)
      assert(!m5.isFeasible)
      assert(m6.isFeasible)
    }
  }
}

class TestMarginsWithCellBounds extends FunSpec {

  //Infeasible
  def m1 = new MarginsWithCellBounds(DenseVector[Int](),
                                     DenseVector[Int](),
                                     DenseMatrix.fill[Int](0,0)(1))
  //Feasible
  def m2 = new MarginsWithCellBounds(DenseVector(Range(1,6).toArray),
                                     DenseVector(Range(1,6).toArray),
                                     DenseMatrix.fill[Int](5,5)(1))
  //Infeasible
  def m3 = new MarginsWithCellBounds(DenseVector(2,1,3),DenseVector(2,2,1,1),
                                     DenseMatrix((1,0,1,0),(0,0,1,4),(0,1,6,2)))
  //Feasible
  def m4 = new MarginsWithCellBounds(DenseVector(2,1,3),DenseVector(2,2,1,1),
                                     DenseMatrix((1,1,1,2),(1,0,1,4),(3,1,6,1)))
  //Feasible
  def m5 = new MarginsWithCellBounds(DenseVector(3,3,2,2,2,1,1,1), DenseVector(5,4,3,3),
                                     DenseMatrix.fill[Int](4,8)(1))

  describe("A MarginsWithCellBounds") {
    it("should correctly determine feasibility") {
      assert(!m1.isFeasible)
      assert(m2.isFeasible)
      assert(m4.isFeasible)
      assert(m5.isFeasible)
    }
    ignore ("should correctly determine feasibility when the flow problem is required") {
      assert(!m3.isFeasible)
    }
  }
}
